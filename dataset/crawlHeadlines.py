from bs4 import BeautifulSoup

import json
import urllib.request
import re

# url = "https://www.allsides.com/unbiased-balanced-news"
leftWingSites = [{"site": "npr", "home": "https://www.npr.org/"},
                 {"site": "pbs", "home": "https://www.pbs.org/newshour/"},
                 {"site": "bbc", "home": "https://www.bbc.com/news"}]
mixedSites = [{"site": "cnn", "home": "https://www.cnn.com/"},
              {"site": "abc", "home": "https://abcnews.go.com/"},
              {"site": "nbc", "home": "https://www.nbcnews.com/"}]
rightWingSites = [{"site": "fox", "home": "https://www.foxnews.com/"},
                  {"site": "glennbeck", "home": "https://www.glennbeck.com/blog/"},
                  {"site": "hannity", "home": "https://www.foxnews.com/category/shows/hannity"}]

dummyLeft = [{"site": "npr", "home": "https://www.npr.org/", "htmllink": "h3", "htmlclass": "title"}]
dummyMixed = [{"site": "nbc", "home": "https://www.nbcnews.com/", "htmllink": "h2", "htmlclass": "headline"}]
dummyRight = [{"site": "fox", "home": "https://www.foxnews.com/", "htmllink": "h3", "htmlclass": "title"}]



# for side in [leftWingSites, mixedSites, rightWingSites]:
for side in [dummyMixed]:
    for entry in side:
        # create a request so we don't look like a python script but like a real browser
        url = entry["home"]
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'})
        
        
        # read the webpage in as an html
        response = urllib.request.urlopen(req)
        content_type = response.getheader('Content-Type')

        html_bytes = response.read()
        # print(content_type)

        html = html_bytes.decode("utf-8")

        # print(html)
        

        # # get headlines
        soup = BeautifulSoup(html, 'html.parser')

        links = soup.find_all('a', {'href': True}) #find all links

        # Find all headlines by searching for <h3> tags with the class "title"
        for link in links: 
            headline = link.find(entry["htmllink"], class_=entry["htmlclass"])

            if headline: 
                # Extract the link inside the <a> tag (if it exists)
                headline_text = headline.get_text()
                headline_link = link['href']

                print(headline_text)
                print(headline_link)
        

#randomized rate limiting when crawling

