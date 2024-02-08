import feedparser
from datetime import datetime
import re
from bs4 import BeautifulSoup
import json

def main():
    
    # https://www.mediawiki.org/w/api.php?action=help&modules=featuredfeed
    rss_url = "https://en.wikipedia.org/w/api.php?action=featuredfeed&feed=featured&feedformat=atom"
    feed = feedparser.parse(rss_url)

    # current date
    dt_now = datetime.now()
    current_date_str = dt_now.now().strftime("%Y%m%d")
    
    #  current feed url
    pattern = re.compile(r'https://en.wikipedia.org/wiki/Special:FeedItem/featured/' + current_date_str + r'\d+/en')

    for entry in feed.entries:
        if pattern.match(entry.link):
            featured_article = entry
            break

    article_details = {}

    if featured_article:
        article_details['feed_link'] = featured_article.link
        article_details['featured_date'] = dt_now.strftime("%Y-%m-%d")
        
        soup = BeautifulSoup(featured_article.summary, 'html.parser')
        
        image = soup.find('img')
        article_details['image_url'] = image['src'] if image else None
        
        first_link = soup.find('a', href=True)
        article_url = first_link['href'] if first_link else None
        if article_url.startswith("/"):
            article_url = "https://en.wikipedia.org" + article_url
        article_details['article_link'] = article_url

        with open('featured_article.json', 'w') as f:
            json.dump(article_details, f, indent=4)

    else:
        print("retrieval failed")

if __name__ == "__main__":
    main()