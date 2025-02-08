import numpy as np
import pickle
import skimage.io as io
import os

import createFilterBank, getVisualWords, getImageFeatures


# -----fill in your implementation here --------
cornerType = "Harris"
dictionary = pickle.load(open('dictionary%s.pkl' % cornerType, 'rb'))

filterBank = createFilterBank.create_filterbank()

traintest = pickle.load(open('../data/traintest.pkl', 'rb'))
train_images = traintest['train_imagenames']
train_labels = traintest['train_labels']

trainFeatures = np.zeros((len(train_images), len(dictionary)))

for i in range(len(train_images)):
    # print(train_images[i])
    I = io.imread("../data/" + train_images[i])
    wordMap = getVisualWords.get_visual_words(I, dictionary, filterBank)
    trainFeatures[i] = np.reshape(getImageFeatures.get_image_features(wordMap, len(dictionary)), -1)

savedDict = {
    "dictionary" : dictionary,
    "filterBank" : filterBank,
    "trainFeatures" : trainFeatures,
    "trainLabels" : train_labels
}


# with open('vision%s.pkl' % cornerType, 'wb') as f:
#             pickle.dump(savedDict, f, protocol=pickle.HIGHEST_PROTOCOL)

# ----------------------------------------------
