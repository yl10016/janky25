from bs4 import BeautifulSoup
from collections import Counter

import urllib.request
import re 

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# leftWingSites = [{"site": "npr", "home": "https://www.npr.org/", "htmllink": "h3", "htmlclass": "title"},
#                  {"site": "pbs", "home": "https://www.pbs.org/newshour/", "htmllink": "h3", "htmlclass": "title"},
#                  {"site": "bbc", "home": "https://www.bbc.com/news", "htmllink": "h3", "htmlclass": "title"}]
# mixedSites = [{"site": "cnn", "home": "https://www.cnn.com/"},
#               {"site": "abc", "home": "https://abcnews.go.com/"},
#               {"site": "nbc", "home": "https://www.nbcnews.com/"}]
# rightWingSites = [{"site": "fox", "home": "https://www.foxnews.com/"},
#                   {"site": "glennbeck", "home": "https://www.glennbeck.com/blog/"},
#                   {"site": "hannity", "home": "https://www.foxnews.com/category/shows/hannity"}]


# this code visits the homepage of a few major news pages, just once each, storing a list of headlines and urls to further information
def crawlHeadlines() : 
    #inspect html to get the htmllink and htmlclass
    leftWingSites = [{"site": "npr", "home": "https://www.npr.org/", "htmllink": "h3", "htmlclass": "title"}]
    mixedSites = [{"site": "nbc", "home": "https://abcnews.go.com/", "htmllink": "h3", "htmlclass": "headline"}]
    rightWingSites = [{"site": "fox", "home": "https://www.foxnews.com/", "htmllink": "h3", "htmlclass": "title"}]

    #declare dictionaries to store headliens and urls
    leftHeadlines = {"text": [], "url": []}
    rightHeadlines = {"text": [], "url": []}
    mixedHeadlines = {"text": [], "url": []}

    # for side in [leftWingSites, mixedSites, rightWingSites]:
    for side in [leftWingSites, mixedSites, rightWingSites]:
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
            html = html_bytes.decode("utf-8")
            # print(html)
        

            # get headlines
            soup = BeautifulSoup(html, 'html.parser')
            headline_text = []
            headline_link = []

            links = soup.find_all('a', {'href': True}) #find all links
            # Find all headlines by searching for <h3> tags with the class "title"
            for link in links: 
                headline = link.find(entry["htmllink"], class_=entry["htmlclass"])

                if headline: 
                    # Extract the link inside the <a> tag (if it exists)
                    headline_text.append(headline.get_text().strip())
                    headline_link.append(link['href'])

            
            # for additional json stored in <scripts> within the html
            scripts = soup.find_all('script')

            for script in scripts:
                if script.string: 
                    matches = re.findall(r'{"headline":"(.*?)".*?","link":"(https://.*?)"', script.string)
                    for match in matches: 
                        if (len(match[0]) > 1 and len(match[1]) > 1): #guard against weird behavior
                            headline_text.append(match[0])
                            headline_link.append(match[1])

        #store in dictionary
        if side == leftWingSites:
            leftHeadlines["text"] += headline_text
            leftHeadlines["url"] += headline_link
        if side == rightWingSites:
            rightHeadlines["text"] += headline_text
            rightHeadlines["url"] += headline_link
        if side == mixedSites:
            mixedHeadlines["text"] += headline_text
            mixedHeadlines["url"] += headline_link

    return leftHeadlines, rightHeadlines, mixedHeadlines


#finds common keywords within headlines across the sites
# def findCommonTopics(leftHeadlines, rightHeadlines, mixedHeadlines):
#     words = [] * len(leftHeadlines)
#     wordCounts = [] * len(leftHeadlines)
#     for i in range(len(leftHeadlines)):
#         words.append(re.findall(r'\b\w+\b', leftHeadlines[i].lower()))
#         wordCounts.append(Counter(words[i]))
#         print(wordCounts[i])


def calculateCosineSimilarity(x, y):
    vectorizer = TfidfVectorizer()
    vectorizer.fit([x,y])
    vector1 = vectorizer.transform([x])
    vector2 = vectorizer.transform([y])
    
    similarity = cosine_similarity(vector1, vector2)[0][0]

    return similarity

# preliminary matching of headlines using cosine similarity between the headline words
def getSimilarHeadlines(leftHeadlines, rightHeadlines, mixedHeadlines, threshold = 0.12):
    similarHeadlines = {"left": [], "right": [], "mid": [], "similarity": []}

    for m in mixedHeadlines:
        for r in rightHeadlines:
            for l in leftHeadlines:
                #calulate three-way cosine similarity
                similaritymr = calculateCosineSimilarity(m,r)
                similarityrl = calculateCosineSimilarity(r,l)
                similarityml = calculateCosineSimilarity(m,l)

                threeWaySimilarity = (similaritymr + similarityrl + similarityml) / 3
                threeWaySimilarity = min(similarityml, similaritymr, similarityrl)
                
                if (threeWaySimilarity > threshold):
                    similarHeadlines["left"].append(l)
                    similarHeadlines["right"].append(r)
                    similarHeadlines["mid"].append(m)
                    similarHeadlines["similarity"].append(threeWaySimilarity)

    print(similarHeadlines)
    return similarHeadlines

                
        
            


    #randomized rate limiting when crawling

