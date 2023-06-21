import Snoowrap from 'snoowrap';
import error from '../utils/error.js';
import BaseError from '../utils/baseError.js';
import codes from '../utils/error.js'
import dotenv from 'dotenv'
dotenv.config();


export class RedditScrape {

    setParams(paramList) {
        return {subreddit : paramList[1]}
    }

    async execute (params) {

        var request = null;

        try{
            request = new Snoowrap({
               userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
               clientId: process.env.REDDIT_CLIENT_ID,
               clientSecret: process.env.REDDIT_SECRET,
               username: process.env.REDDIT_USERNAME,
               password: process.env.REDDIT_PASSWORD
           })
       }catch(err) {
          Logger.error(err)
           throw new BaseError("Reddit Initialization Error", codes.SERVER_ERROR, err.message)
       }

       let {subreddit} = params

        let itemArr = []

       try{

            const posts = await request.getSubreddit(subreddit).getNew()

            itemArr = posts.map(post => ({
                title: encodeURIComponent(post.title),
                url: encodeURIComponent(`https://www.reddit.com${post.permalink}`)
            }))

            return itemArr

       }catch(err) {
            Logger.error(err)
            throw new BaseError(err.name, codes.SERVER_ERROR, err.message)
       }finally {
            Logger.info(`Scraper Completed at ${new Date()} for subreddit: ${subreddit}`)
       }

    }
}