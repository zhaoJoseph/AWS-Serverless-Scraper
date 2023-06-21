import error from '../utils/error.js';
import BaseError from '../utils/baseError.js';
import codes from '../utils/error.js'
import dotenv from 'dotenv'
dotenv.config();

export class Scraper {
    constructor() {
      this.strategy = null;
    }
  
    setStrategy(strategy) {
      this.strategy = strategy;
    }
  

    async scrape(params) {
      if (!this.strategy) {
        throw new Error('No strategy set.');
      }
  
      try{
        
        const results = await this.strategy.execute(params, this.driver);
        return results;

      } catch (err) {
        Logger.error(err)
        throw new BaseError(err.name, codes.SERVER_ERROR, err.message)
      }
      }
  }


