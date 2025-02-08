import numpy as np


def get_image_features(wordMap, dictionarySize):

    # -----fill in your implementation here --------
    h = np.zeros((dictionarySize, 1))

    flattenedWordMap = np.ndarray.flatten(wordMap)
    for i in range(len(flattenedWordMap)):
        h[flattenedWordMap[i]] += 1
    
    #normalize
    hmin = np.min(h)
    hmax = np.max(h)
    h = (h - hmin) / (hmax - hmin)
    # ----------------------------------------------
    
    return h
