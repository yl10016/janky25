import crawlHeadlines
import numpy as np
import pickle
import random

# will eventually: generate a set of headlines to compare, with a quick summary of viewpoints
def generate(refresh, recomputeDictionary):
    left, right, mixed = crawlHeadlines.crawlHeadlines()

    if (refresh): #falsed out during testing phase
        similarHeadlines = crawlHeadlines.getSimilarHeadlines(left, right, mixed)
        crawlHeadlines.populateBlurbs(similarHeadlines)
        crawlHeadlines.recomputeSimilarities(similarHeadlines, threshold=0.4)

        if (recomputeDictionary):
            with open("similarHeadlines.pkl", "wb") as f:
                pickle.dump(similarHeadlines, f)

    with open("similarHeadlines.pkl", "rb") as f:
        similarHeadlines = pickle.load(f)
    
    print(f":{similarHeadlines["similarity"]}")

    #choose a headline
    chosenIndex = random.randint(0, len(similarHeadlines))    
    print(similarHeadlines["left"][chosenIndex])
    print(similarHeadlines["right"][chosenIndex])
    print(similarHeadlines["mid"][chosenIndex])

    crawlHeadlines.writeToCsv(similarHeadlines, chosenIndex)
            

    # for i in range(len(similarHeadlines["left"])):
    #     print(similarHeadlines["left"][i])
    #     print(similarHeadlines["right"][i])
    #     print(similarHeadlines["mid"][i])
    #     print(similarHeadlines["similarity"][i])
    #     print()

    # print(f":{similarHeadlines["similarity"]}")



# run pipeline with a call to generate
refresh = False
recomputeDictionary = True
generate(refresh, recomputeDictionary)
