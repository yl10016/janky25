import generateUtil 
import numpy as np
import pickle
import random

# will eventually: generate a set of headlines to compare, with a quick summary of viewpoints
def generate(refresh):
    left, right, mixed = generateUtil.crawlHeadlines()

    if (refresh): #falsed out during testing phase
        similarHeadlines = generateUtil.getSimilarHeadlines(left, right, mixed)
        generateUtil.populateBlurbs(similarHeadlines)
        generateUtil.recomputeSimilarities(similarHeadlines, threshold=0.4)

        if (False):
            with open("similarHeadlines.pkl", "wb") as f:
                pickle.dump(similarHeadlines, f)

    with open("similarHeadlines.pkl", "rb") as f:
        similarHeadlines = pickle.load(f)
    
    #choose a headline
    chosenIndex = random.randint(0, len(similarHeadlines)-1)    
    # print(similarHeadlines["left"][chosenIndex])
    # print(similarHeadlines["right"][chosenIndex])
    # print(similarHeadlines["mid"][chosenIndex])

    generateUtil.writeToCsv(similarHeadlines, chosenIndex)

    # for i in range(len(similarHeadlines["left"])):
    #     print(similarHeadlines["left"][i])
    #     print(similarHeadlines["right"][i])
    #     print(similarHeadlines["mid"][i])
    #     print(similarHeadlines["similarity"][i])
    #     print()

    # print(f":{similarHeadlines["similarity"]}")



# run pipeline with a call to generate
refresh = False
generate(refresh)
