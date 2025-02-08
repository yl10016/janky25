import skimage.io as io
import cv2
import numpy as np
import skimage

import extractFilterResponses
import createFilterBank
import getRandomPoints
import getHarrisPoints
import getDictionary
import getImageFeatures
import getImageDistance

import matplotlib.pyplot as plt
import getVisualWords

import os 
import pickle



# I = io.imread("../data/desert/sun_adpbjcrpyetqykvt.jpg") #task 3.1
# I = io.imread("../data/rainforest/sun_aakdsiijvzzclecx.jpg") #task 3.2
# I = io.imread("../data/airport/sun_aesovualhburmfhn.jpg") #task 4.1
I = io.imread("../data/airport/sun_afrhwhqnsmfkhirs.jpg")
# I = io.imread("../data/airport/sun_aflgtvhkyftqgkgx.jpg")
 
filterBank = createFilterBank.create_filterbank()
filterResponses = extractFilterResponses.extract_filter_responses(I, filterBank)
print(I.shape)

#task 3.1
i=34
img = filterResponses[:,:,i]

#show image
clippedImg = img
# cv2.imshow('test' + str(i) + '.png', clippedImg.astype(np.uint8))

#task 3.2
alpha = 500
k = 0.05
points1 = getRandomPoints.get_random_points(I, alpha)
points2 = getHarrisPoints.get_harris_points(I, alpha, k)


#plot points2
for (y,x) in points2:
    plt.plot(x,y, marker="v", markersize=1, color="red")
plt.imshow(I)
# plt.show()


#task 3.3
alpha = 50
K = 100 #words
imagePaths = ["airport/sun_aerinlrdodkqnypz.jpg", 
              "airport/sun_aerprlffjscovbbc.jpg",
              "airport/sun_aflgtvhkyftqgkgx.jpg"]
path = "../data"

# imagePaths = []
# for directory in (os.listdir(path)):
#     if (not directory.endswith(".pkl")): #not a directory
#         for fileF in (os.listdir(path + "/" + directory)):
#             if (fileF.endswith(".jpg")): #is an image
#                 imagePaths.append(directory + "/" + fileF)
    

# dictionaryHarris = getDictionary.get_dictionary(imagePaths, alpha, K, "Harris")
# # print(dictionaryHarris)
# # save to pickle
# with open('dictionaryHarris.pkl', 'wb') as f:
#     pickle.dump(dictionaryHarris, f, protocol=pickle.HIGHEST_PROTOCOL)

# dictionaryRandom = getDictionary.get_dictionary(imagePaths, alpha, K, "Random")
# with open('dictionaryRandom.pkl', 'wb') as f:
#     pickle.dump(dictionaryRandom, f, protocol=pickle.HIGHEST_PROTOCOL)

# print(dictionaryRandom)


#4.1 
dictionary = pickle.load(open('dictionary%s.pkl' % "Random", 'rb'))

wordMap = getVisualWords.get_visual_words(I, dictionary, filterBank)
coloredImg = skimage.color.label2rgb(wordMap, I, alpha=.8)
plt.imshow(coloredImg)
plt.axis("off")
plt.show()

#4.2
histogram = getImageFeatures.get_image_features(wordMap, len(dictionary))
label = dictionary[np.argmax(histogram)]
# print(label)
# print(np.argmax(histogram))

#5.1
dictionaries = pickle.load(open('vision%s.pkl' % "Harris", 'rb'))
Hset = dictionaries["trainFeatures"]

# distancesEuc = getImageDistance.get_image_distance(histogram, Hset, "euclidean")
# print(distancesEuc)
# distancesChi = getImageDistance.get_image_distance(histogram, Hset, "chi2")
# print(distancesChi)



#close when 0 is pressed
# cv2.waitKey(0)