import error from '../utils/error.js';
import BaseError from '../utils/baseError.js';
import codes from '../utils/error.js'
import dotenv from 'dotenv'
import {Builder, By, Key, until} from 'selenium-webdriver'
import firefox from 'selenium-webdriver/firefox.js'
import { PageLoadStrategy } from 'selenium-webdriver/lib/capabilities.js'
import { TimeoutError } from 'selenium-webdriver/lib/error.js';
import Logger from '../utils/logger.js';
dotenv.config();

export class HTMLGridScrape {
    
    setParams(paramList) {
        return {url : paramList[0], className: paramList[1]}
    }

    async setDriver() {
  
      var agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246', 
      'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36',
      'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9',
      'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:15.0) Gecko/20100101 Firefox/15.0.1']

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
          
      firefoxOptions.setPreference('general.useragent.override', agents[Math.floor(Math.random() * agents.length)]);
    
      const driver = await new Builder().forBrowser('firefox')
      .setFirefoxOptions(firefoxOptions)
      .build()
    
      driver.manage().setTimeouts({pageLoad: 30000, implicit: 10000});
    
      return driver;
    
    }

    async execute(params) {

        const LIMIT = 1000;

        const { url, className } = params;

        var driver = null;

        var count = 0;

        let itemArr = [];             

        var attempts = 0;

      while(attempts < 3){

        try{
        
            driver = await this.setDriver();

            await driver.get(url);

            await new Promise(resolve => setTimeout(resolve, 10000));

            var elements = await driver.wait(until.elementsLocated(By.className(className)), 30000, 'Timed out after 30 seconds', 5000);

            // It just takes a really long time to load the whole page

            if(await elements[elements.length - 1].getAttribute('innerText') == '') {

            while(count < LIMIT && (await elements[elements.length - 1].getAttribute('innerText') == '')) {
                elements = await driver.wait(until.elementsLocated(By.className(className),10000))
                await driver.executeScript("arguments[0].scrollIntoView();", elements[elements.length - 1])
                await driver.executeScript("document.documentElement.scrollTo({top: 0, behavior: 'smooth'}); setTimeout(() => { window.scrollTo({ top: 0 }); }, 2000);");
                await driver.executeScript("arguments[0].scrollIntoView();", elements[elements.length - 1])
                count += 1
                elements = await driver.wait(until.elementsLocated(By.className(className)))
            }
            }

            if(elements.length < 1) {
                 throw new BaseError("No grid found", error.codes.SERVER_ERROR, "No grid found")
            }

            const elementPromises = elements.map(async (element) => {
                const title = (await element.getAttribute('innerText')).toString().split('/\s+/').join(' ').replace(/'/g, '').replace(/\s+/g, ' ');
              
                if (title.trim() !== '') {
                 
                  var href = '';
                  var encodedURL = '';

                  var tagName = await element.getTagName();

                try{
                    if(tagName === 'a') {
                        href = await element.getAttribute('href');
                        encodedURL = await encodeURIComponent(href);
    
                      }else{
                        href = await element.findElement(By.css('a[href]'));
                        encodedURL = await encodeURIComponent(await href.getAttribute('href'));
                    }

                }catch(error){
                    encodedURL = await encodeURIComponent(url);
                }

                  const encodedTitle = await encodeURIComponent(title)
                  return { title: encodedTitle , url : encodedURL};
                }
                return null;
              });
              
            itemArr = await Promise.all(elementPromises.filter((item) => item != null));

    } catch (err) {

      Logger.error(err)

        if(err instanceof TimeoutError){
          Logger.info(`Attempt ${attempts + 1} timed out. Retrying...`);
          attempts++;
        }else if (err.statusCode) {
          throw new BaseError(err.error, err.statusCode, err.error);
        } else {
          throw new BaseError(err.name, codes.SERVER_ERROR, err.message);
        }
      }finally{
        if((attempts == 0)  || (attempts >= 3)){
        await driver.quit();
        Logger.info(`Scraper Completed at ${new Date()} for site: ${url}`);

          if(attempts >= 3){
            throw new BaseError(new TimeoutError(), 1, "Timed out after 3 tries.")
          }

        return itemArr;
        }
      }
    }
  }

}
