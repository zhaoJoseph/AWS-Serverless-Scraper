from apiscraper.apiscraper import ApiScraper
from praw import Reddit
from os import environ as env
from dotenv import load_dotenv

class RedditApi(ApiScraper):

    def __init__(self, subreddit):
        load_dotenv()
        self.subreddit = subreddit
        self.reddit = Reddit(
            client_id=env['REDDIT_CLIENT_ID'],
            client_secret=env['REDDIT_SECRET'],
            password=env['REDDIT_PASSWORD'],
            user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64; rv:12.0) Gecko/20100101 Firefox/12.0',
            username=env['REDDIT_USERNAME']
        )

    def get(self):
        posts = self.reddit.subreddit(self.subreddit).hot(limit=10)
        return posts

    def collect(self, data):
        for post in data:
            yield {
                'title':  post.title,
                'url': self.reddit.config.reddit_url + post.permalink
            }
