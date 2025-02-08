import numpy as np
import pickle
import getImageDistance
import getVisualWords
import getImageFeatures
import skimage.io as io

# -----fill in your implementation here --------
traintest = pickle.load(open('../data/traintest.pkl', 'rb'))
test_imagenames = traintest['test_imagenames']
test_labels = traintest['test_labels']

# for testing
# test_imagenames = test_imagenames[0:50]
# test_labels = test_labels[0:50]

def computeVariation(cornerMetric, distanceType):
    pkl = pickle.load(open('vision%s.pkl' % cornerMetric, 'rb'))
    train_histograms = pkl["trainFeatures"]
    dictionary = pkl["dictionary"]
    filterBank = pkl["filterBank"]
    train_labels = pkl["trainLabels"]

    correctCount = 0
    C = np.zeros((8,8))
    for i in range(len(test_imagenames)):
        #compute image histogram
        I = io.imread("../data/" + test_imagenames[i])
        test_wordMap = getVisualWords.get_visual_words(I, dictionary, filterBank)
        test_histograms = getImageFeatures.get_image_features(test_wordMap, len(dictionary))

        #get nearest label
        test_imageDist = getImageDistance.get_image_distance(test_histograms, train_histograms, distanceType)
        test_nearestHistogramIndex = np.argmin(test_imageDist)
        test_label = int(train_labels[test_nearestHistogramIndex]) - 1 #index from 0
        actual_label = int(test_labels[i]) - 1 #index from 0

        #increment stats
        C[actual_label, test_label] += 1
        if test_label == actual_label:
            correctCount += 1
    
    print("\n%s corner detection, %s distance " % (cornerMetric, distanceType))
    print("Accuracy: %i correct / %i total = %f" % (correctCount, len(test_imagenames), (correctCount / len(test_imagenames))))
    print("Confusion matrix:")
    print(C)
        
computeVariation("Random", "euclidean")
computeVariation("Random", "chi2")
computeVariation("Harris", "euclidean")
computeVariation("Harris", "chi2")

# ----------------------------------------------
