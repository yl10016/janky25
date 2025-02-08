import numpy as np
import skimage.io as io
import pickle
import getVisualWords, getImageDistance, getImageFeatures
import matplotlib.pyplot as plt

# -----fill in your implementation here --------
cornerMetric = "Random"
distanceType = "chi2"

# load in test data
traintest = pickle.load(open('../data/traintest.pkl', 'rb'))
test_imagenames = traintest['test_imagenames']
test_labels = traintest['test_labels']

# for testing
# test_imagenames = test_imagenames[0:20]
# test_labels = test_labels[0:20]

# load in trained data
pkl = pickle.load(open('vision%s.pkl' % cornerMetric, 'rb'))
train_histograms = pkl["trainFeatures"]
dictionary = pkl["dictionary"]
filterBank = pkl["filterBank"]
train_labels = pkl["trainLabels"]

k = 40
#k+1 so i can have the plot correctly indexed from 1-k
accuracies = np.zeros((k+1, 1))
labels = np.zeros((k+1, len(test_imagenames)))
Cmatrices = np.zeros((8,8,k+1))

for n in range(1, k+1):
    correctCount = 0
    C = np.zeros((8,8))
    for i in range(len(test_imagenames)):
        #compute image histogram
        I = io.imread("../data/" + test_imagenames[i])
        test_wordMap = getVisualWords.get_visual_words(I, dictionary, filterBank)
        test_histograms = getImageFeatures.get_image_features(test_wordMap, len(dictionary))

        #get n nearest labels
        test_imageDist = getImageDistance.get_image_distance(test_histograms, train_histograms, distanceType)
        test_nearestIndices = np.argpartition(test_imageDist, n)[:n] #first n smallest elements
        test_klabels = train_labels[test_nearestIndices]
        test_klabels = test_klabels.astype(int) #to make sure indicing works
        
        #take majority vote
        # print(test_nearestIndices)
        counts = np.bincount(test_klabels)
        # print(test_klabels)
        test_label = np.argmax(counts) - 1 #index from 0, majority vote
        # print(test_label)
        actual_label = int(test_labels[i]) - 1 #index from 0

        #increment stats
        C[actual_label, test_label] += 1
        if test_label == actual_label:
            correctCount += 1
    
    accuracies[n] = correctCount / len(test_imagenames)
    Cmatrices[:,:,n] = C

print("\n%s corner detection, %s distance " % (cornerMetric, distanceType))
bestIndex = np.argmax(accuracies)
bestAccuracy = accuracies[bestIndex]
print("Best Accuracy: = %f" % bestAccuracy)
print("Confusion matrix:")
print(Cmatrices[:,:,bestIndex])

#plot accuracies
xpoints = np.arange(k+1)
plt.plot(xpoints[1:], accuracies[1:]) # not include k=0

plt.show()

# ----------------------------------------------
