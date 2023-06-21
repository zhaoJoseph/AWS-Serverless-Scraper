import funcs from './scraper/aggregator.js'
import async from 'async'
import readline from 'readline'
import { Scraper } from './scraper/scrapeStrategies.js'
import { TwitterScrape } from './scraper/Strategies/TwitterScrape.js'
import { RedditScrape } from './scraper/Strategies/RedditScrape.js'
import { HTMLGridScrape } from './scraper/Strategies/HTMLGridScrape.js'
import fs from 'fs'

const gridScrape = new HTMLGridScrape();
const twitterScrape = new TwitterScrape();
const redditScrape = new RedditScrape();

// List of strategies
let strategies = {
    "grid" : gridScrape,
    "twitter" : twitterScrape,
    "reddit" : redditScrape,
}

import dotenv from 'dotenv'
dotenv.config()

const { PORT, FILENAME } = process.env;

//###################################################//
//                  SCRAPER                          //
//###################################################//

async function startScraper() {

    // Initialize scraper driver
    const scraper = new Scraper()
    
    // Initialize queue for async scraping
    const siteQueue = async.queue(async (siteUrl) => {
        const result = await scrapeSite(siteUrl)
        await funcs.aggregateData(result)
    }, 1)
    
    await processSites()
    
    async function processSites() {

        // read file stream
        const stream = fs.createReadStream(`${FILENAME}`, {encoding: 'utf8'})
        const rl = readline.createInterface({
        input: stream,
        crlfDelay: Infinity
        });
    
        for await (const line of rl) {
        // Add each site to the queue
        siteQueue.push(line.trim());
        }
        
    }
    
    async function scrapeSite(line) {

        // Initialize parameters for each strategy
        const args = line.split(',');
        scraper.setStrategy(strategies[args[1]])
        const paramList = [args[0]].concat(args.slice(2))
        const params = scraper.strategy.setParams(paramList)

        // Scrape site
        const scraped_data = await scraper.scrape(params)
        return scraped_data
    }

}
    
    
await startScraper();