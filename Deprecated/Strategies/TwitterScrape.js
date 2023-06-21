import error from '../utils/error.js';
import BaseError from '../utils/baseError.js';
import codes from '../utils/error.js'
import dotenv from 'dotenv'
import {Builder, By, Key, until} from 'selenium-webdriver'
import { Actions } from 'selenium-webdriver/lib/input.js';
import firefox from 'selenium-webdriver/firefox.js'
import { PageLoadStrategy } from 'selenium-webdriver/lib/capabilities.js'
import Logger from '../utils/logger.js';
dotenv.config();

export class TwitterScrape {

    setParams(paramList) {
        return {url : paramList[0], username: paramList[1]}
    }

    async setDriver() {
  
      var agents = ['Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36']

      // Create a Firefox options object with additional arguments
      let firefoxOptions = new firefox.Options();
      firefoxOptions.addArguments('--disable-gpu',
                                  '--no-sandbox',
                                  '--headless',
                                  '--disable-dev-shm-usage',
                                  '--disable-renderer-backgrounding',
                                  '--disable-background-timer-throttling',
                                  "--disable-backgrounding-occluded-windows",
                                  "--disable-client-side-phishing-detection",
                                  '--disable-browser-side-navigation'
                                  );
      firefoxOptions.setPageLoadStrategy(PageLoadStrategy.NONE);
          
      firefoxOptions.setPreference('general.useragent.override', agents[0]);
    
      const driver = await new Builder().forBrowser('firefox')
      .setFirefoxOptions(firefoxOptions)
      .build()
    
      driver.manage().setTimeouts({pageLoad: 30000, implicit: 10000});
    
      return driver;
    
    }

    async scrollPage(driver) {
      await driver.executeScript('window.scrollTo(0, document.body.scrollHeight);');
      await driver.sleep(2000); // Wait for the page to scroll and load more tweets (adjust as needed)
    }

    async click(driver) {
      const actions = new Actions(driver);
      await actions.move({ x: 100, y: 200 }).click().perform();
    }

    async execute (params){

        let {url, username} = params

        var driver = null;

        try{
        
          driver = await this.setDriver();

          await driver.get(url);
          await driver.sleep(3000); // Wait for the page to load (adjust as needed)
      
          // Scroll to the bottom of the page to load more tweets (repeat as necessary)
          await this.scrollPage(driver);
          await this.scrollPage(driver);
          // You can add more scrollPage() calls if needed to load additional tweets
      
          await driver.wait(until.elementsLocated(By.css('article[data-testid="tweet"]'),3000))

          await driver.sleep(20000)

          await this.click(driver)

          const tweetResults = await driver.findElements(By.css('article[data-testid="tweet"]'));

          var tweets = []

          for (let i = 0; i < tweetResults.length; i++) {
            // check if the user who wrote the post is the page owner, not a retweet

            // skip special tweets or retweets, user cells and show more option
            const specialTweet = await tweetResults[i].findElements(By.css('div[data-testid="socialContext"]'));            

            if(specialTweet.length > 0) {
              continue;
            }

            // Check if the user posted the tweet or retweet
            const handler = await tweetResults[i].findElements(By.css('div[data-testid="User-Name"]'));
            const handlerName = await handler[0].getText();
            if (handlerName.includes(`@${username}`)) {
              const tweetTextElement = await tweetResults[i].findElements(By.css('div[data-testid="tweetText"]'));
              const tweetText = await tweetTextElement[0].getText();
              const postId = await tweetResults[i].findElements(By.css('a.r-qvutc0'));
              const id = await postId[0].getAttribute("href");

              tweets.push({
                title: encodeURIComponent(tweetText),
                url: encodeURIComponent(id)
              })
            }
          }

          return tweets

        }catch(err){
          console.log(err)
          Logger.error(err)
          throw new BaseError(err.name, codes.SERVER_ERROR, err.message)

        } finally {
          await driver.quit();
          Logger.info(`Scraper Completed at ${new Date()} for twitter page: ${username}`)
        }

    }

}
