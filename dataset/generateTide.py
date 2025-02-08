import crawlHeadlines
import numpy as np
import pickle
import random

# will eventually: generate a set of headlines to compare, with a quick summary of viewpoints

if (False): #falsed out during testing phase
    left, right, mixed = crawlHeadlines.crawlHeadlines()
    # crawlHeadlines.findCommonTopics(left["text"], right["text"], mixed["text"])
    similarHeadlines = crawlHeadlines.getSimilarHeadlines(left["text"], right["text"], mixed["text"])
    # with open("similarHeadlines.pkl", "wb") as f:
    #     pickle.dump(similarHeadlines, f)

with open("similarHeadlines.pkl", "rb") as f:
    similarHeadlines = pickle.load(f)

#choose a headline
chosenIndex = random.randint(0, len(similarHeadlines))    

print(similarHeadlines["left"][chosenIndex])
print(similarHeadlines["right"][chosenIndex])
print(similarHeadlines["mid"][chosenIndex])