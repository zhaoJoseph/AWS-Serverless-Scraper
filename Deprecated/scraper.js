class Scraper {

    async scrape(strategy) {
        try{
            return await JSON.stringify(strategy.scrape());
        }catch(err){
            console.log(err)
        }
    }
}

module.exports = Scraper;