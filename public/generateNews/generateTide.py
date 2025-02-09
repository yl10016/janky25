import generateUtil 
import numpy as np
import random

# will eventually: generate a set of headlines to compare, with a quick summary of viewpoints
def generate(refresh):
    left, right, mixed = generateUtil.crawlHeadlines()

    if (refresh): #falsed out during testing phase
        similarHeadlines = generateUtil.getSimilarHeadlines(left, right, mixed)
        generateUtil.populateBlurbs(similarHeadlines)
        generateUtil.recomputeSimilarities(similarHeadlines, threshold=0.4)
    
    #choose a headline
    chosenIndex = random.randint(0, len(similarHeadlines)-1)   
    generateUtil.writeToCsv(similarHeadlines, chosenIndex)

# run pipeline with a call to generate
generate(True)
