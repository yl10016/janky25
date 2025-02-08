from bs4 import BeautifulSoup
from collections import Counter

import urllib.request
import re 
import csv
import random

#for cosine similarity
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
            # print(soup.prettify())
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
            
            # for h3 in soup.find_all('article'):
            #     print(h3.text, h3.get('class'))
            
            # links = soup.find_all(entry["htmllink"], class_=entry["htmlclass"]) #find all links
            # # Find all headlines by searching for <h3> tags with the class "title"
            # # print(len(links))
            # for link in links: 
            #     headline = link.find('a') # if <a> is contained within the <href> things instead

            #     if headline: 
            #         # Extract the link inside the <a> tag (if it exists)
            #         headline_text.append(headline.get_text().strip())
            #         headline_link.append(headline['href'])

            
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

    # print(f":{leftHeadlines["text"]}")
    # print(f":{rightHeadlines["text"]}")
    # print(f":{mixedHeadlines["text"]}")
    return leftHeadlines, rightHeadlines, mixedHeadlines


def calculateCosineSimilarity(x, y):
    vectorizer = TfidfVectorizer()
    vectorizer.fit([x,y])
    vector1 = vectorizer.transform([x])
    vector2 = vectorizer.transform([y])
    
    similarity = cosine_similarity(vector1, vector2)[0][0]

    return similarity

def calculateThreewaySimilarity(l, r, m, useMinimum=True):
    similaritymr = calculateCosineSimilarity(m,r)
    similarityrl = calculateCosineSimilarity(r,l)
    similarityml = calculateCosineSimilarity(m,l)

    if useMinimum:
        threeWaySimilarity = min(similarityml, similaritymr, similarityrl)
    else:
        threeWaySimilarity = (similaritymr + similarityrl + similarityml) / 3

    return threeWaySimilarity

# preliminary matching of headlines using cosine similarity between the headline words
def getSimilarHeadlines(leftHeadlines, rightHeadlines, mixedHeadlines, threshold = 0.12):
    similarHeadlines = {"left": [], "lefturl": [], "leftblurb": [],
                        "right": [], "righturl": [], "rightblurb": [],
                        "mid": [], "midurl": [], "midblurb": [],
                        "similarity": []}
    for midx in range(len(mixedHeadlines["text"])):
        for ridx in range(len(rightHeadlines["text"])):
            for lidx in range(len(leftHeadlines["text"])):
                #calulate three-way cosine similarity
                m = mixedHeadlines["text"][midx]
                r = rightHeadlines["text"][ridx]
                l = leftHeadlines["text"][lidx]

                threeWaySimilarity = calculateThreewaySimilarity(l, r, m, useMinimum=True)
                
                if (threeWaySimilarity > threshold):             
                    similarHeadlines["mid"].append(m)
                    similarHeadlines["midurl"].append(mixedHeadlines["url"][midx])
                    similarHeadlines["right"].append(r)
                    similarHeadlines["righturl"].append(rightHeadlines["url"][ridx])
                    similarHeadlines["left"].append(l)
                    similarHeadlines["lefturl"].append(leftHeadlines["url"][lidx])
                    similarHeadlines["similarity"].append(threeWaySimilarity)

    # print(similarHeadlines)
    return similarHeadlines


#do another iteration of this? but reading like the first x amount of words in the article       

# populates dictionary of given index for all three news articles with the content of the news article      
# NOTE: assumes same length for all three 
def populateBlurbsIdx(headline, idx):
    urlArray = [headline["lefturl"][idx], headline["righturl"][idx], headline["midurl"][idx]]
    for i in range(3):
        url = urlArray[i]

        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9'})
                
        # read the webpage in as an html
        response = urllib.request.urlopen(req)

        html_bytes = response.read()
        html = html_bytes.decode("utf-8")

        soup = BeautifulSoup(html, 'html.parser')
        article = ""
        paragraphs = soup.find_all('p')  # Find all paragraph tags
        for p in paragraphs:
            article += " " + p.get_text(strip=True)  # Extract and print the text content    

        if i == 0: 
            headline["leftblurb"].append(article)
        elif i == 1:
            headline["rightblurb"].append(article) 
        else:
            headline["midblurb"].append(article)   

#populates all idx in dictionary with news article  
def populateBlurbs(headline):
    print(len(headline["left"]))
    for i in range(len(headline["left"])):
        populateBlurbsIdx(headline, i)

#overwrite headline similarities with similarities from the actual article
def recomputeSimilarities(dictionary, threshold=0.4):
    for idx in range(len(dictionary["left"])):
        #calulate three-way cosine similarity
        m = dictionary["midblurb"][idx]
        r = dictionary["rightblurb"][idx]
        l = dictionary["leftblurb"][idx]

        threeWaySimilarity = calculateThreewaySimilarity(l, r, m, useMinimum=False)
          
        dictionary["similarity"][idx] = threeWaySimilarity
    
    # delete entries that are below threshold
    i = 0
    while i < len(dictionary["left"]):
        if dictionary["similarity"][i] < threshold:
            for k in dictionary.keys():
                del dictionary[k][i]
        else:
            i += 1
    
    return dictionary

# reads our temporary image csv file into an array
def readCsvRowsToArray(filePath):
    array = []
    with open(filePath, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            array.append(row[0]) #only one thing per row
    return array

def getRandomImage(imageArray, num):
    indices = random.sample(range(0, len(imageArray)), num) #inclusive both sides
    return [imageArray[i] for i in indices]


#finds common keywords within headlines across the sites, biased towards words in headlines
def getCommonKeywords(dictionary, articleIndex):
    stopWords = readCsvRowsToArray('englishStopWords.csv')
    blacklistedWords = readCsvRowsToArray('blacklistedWords.csv')
    words = []
    #count words in blurb + heading
    countWords = dictionary["leftblurb"][articleIndex] 
    countWords += " " + dictionary["rightblurb"][articleIndex] 
    countWords += " " + dictionary["midblurb"][articleIndex] 
    
    words.extend(re.findall(r'\b\w+\b', countWords.lower())) 
    wordCounts = Counter(words)

    # bias towards words in headline
    headlineBoost = 2  # Boost factor for headline words
    headlines = dictionary["left"][articleIndex] + " " + dictionary["right"][articleIndex] + " " + dictionary["mid"][articleIndex]
    for word in headlines:
        wordCounts[word] += headlineBoost

    #filter stop words out of the running
    filteredWordCounts = {key: value for key, value in wordCounts.items() 
                          if key not in stopWords and key not in blacklistedWords and len(key) > 1 }
    sortedWordCounts = dict(sorted(filteredWordCounts.items(), key=lambda item: item[1], reverse=True))
    # topThreeWords = list(sortedWordCounts.items())[:3]
    topThreeWords = [word for word, count in list(sortedWordCounts.items())[:3]]
    return topThreeWords

#puts blurb in correct format for display-- remove tabs
def formatStringForCsv(string, appendZeroes=False):
    string = string.replace("\t", "")
    string = string.replace("\n", " ")
    string = re.sub(r'\s{2,}', ' ', string) #replace strings in a row
    if appendZeroes:
        string += "..."
    return string 

#writes appropriate chosen topic to a csv file
def writeToCsv(dictionary, idx): 
    fieldNames = ['id', 'title', 'summary', 'link', 'image']
    fileName = 'generatedTide.csv'
    imageFilePath = 'randomImages.csv'
    blurblength = 200
    
    images = readCsvRowsToArray(imageFilePath)
    randomImages = getRandomImage(images, 3)

    dataDictionary = [{'id': '1', 'title': formatStringForCsv(dictionary["left"][idx]), 
                        'summary': formatStringForCsv(dictionary["leftblurb"][idx][:blurblength], True), 
                        'link': dictionary["lefturl"][idx], 'image':randomImages[0]},
                      {'id': '3', 'title': formatStringForCsv(dictionary["right"][idx]), 
                        'summary': formatStringForCsv(dictionary["rightblurb"][idx][:blurblength], True), 
                        'link': dictionary["righturl"][idx], 'image': randomImages[1]},
                      {'id': '2', 'title': formatStringForCsv(dictionary["mid"][idx]), 
                        'summary': formatStringForCsv(dictionary["midblurb"][idx][:blurblength], True), 
                        'link': dictionary["midurl"][idx], 'image': randomImages[2]}]
    
    
    with open(fileName, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldNames, delimiter='\t') 
        writer.writeheader() 
        writer.writerows(dataDictionary) 
    
    topThreeWords = getCommonKeywords(dictionary, idx)
    capitalizedWords = [word.capitalize() for word in topThreeWords]
    formattedString = ', '.join(capitalizedWords[:-1]) + ' and ' + capitalizedWords[-1] + "\n"
   
    with open('commonTopic.txt', 'w') as file:
        file.write(formattedString)

        
