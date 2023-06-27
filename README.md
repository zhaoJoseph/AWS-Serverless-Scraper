# Serverless Web Scraper
Serveless Web Scraper using AWS services such as batch and cloudwatch

<div align="center">
    <img src="/screenshots/screen1.jpg" width="400px"</img> 
</div>

# Description
Python based web scraper that uses scrapy framework alongside playwight plugin to perform webscraping.
Built to be deployed in AWS services, triggered via lambda function in aws folder.

# Getting Started
## Dependencies
- Python 3.10.11
- Pip
- Linux
- Git

## Installing
- git clone repository
- cd into repo
- activate virtual environment (source pyscraper/venv/bin/activate )
- pip install -r requirements.txt

## Running
- cd repo
- python pyscraper/pyscraper.py [URL]

## Testing
- cd repo
- cd pyscraper
- playwright install
- pytest tests/testpyscrape.py -v  --forked
