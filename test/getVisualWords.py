import numpy as np
from scipy.spatial.distance import cdist
from extractFilterResponses import extract_filter_responses


def get_visual_words(I, dictionary, filterBank):
    # map each pixel to its closest word in the dictionary
    # dictionary = 100 words, each with dimension 60 across each filter
    # -----fill in your implementation here --------
    #run image through the filters
    filterResponses = extract_filter_responses(I, filterBank)

    #flatten filterResponses to be a 2d array
    values = filterResponses.reshape((len(I) * len(I[0]), -1))

    result = cdist(values, dictionary, metric="euclidean")  
    minDistances = np.argmin(result, axis=1) 

    wordMap = minDistances.reshape((len(I), len(I[0])))   
    # ----------------------------------------------

    return wordMap

