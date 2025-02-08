import numpy as np
import cv2 as cv
from createFilterBank import create_filterbank
from extractFilterResponses import extract_filter_responses
from getRandomPoints import get_random_points
from getHarrisPoints import get_harris_points
from sklearn.cluster import KMeans


def get_dictionary(imgPaths, alpha, K, method):

    filterBank = create_filterbank()

    pixelResponses = np.zeros((alpha * len(imgPaths), 3 * len(filterBank)))
    k = 0.05
    for i, path in enumerate(imgPaths):
        print('-- processing %d/%d' % (i, len(imgPaths)))
        image = cv.imread('../data/%s' % path)
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)    # convert the image from bgr to rgb, OpenCV use BGR by default
        
        # -----fill in your implementation here --------
        #apply filter bank
        filterResponses = extract_filter_responses(image, filterBank)

        #get alpha points
        if (method == "Random"):
            points = get_random_points(image, alpha)
        else: 
            points = get_harris_points(image, alpha, k)
        points = np.array(points) #cast to array

        # pixelResponses[:,i] = filterResponses[points]
        # print(pixelResponses.shape)

        #get corresponding values for each point from the filtered images
        responses = np.array([filterResponses[x,y] 
                              for (x,y) in points])
        
        # print(responses)
        # print("then i get==")
        # print(filterResponses)
        #accumulate results in pixelResponses
        for j in range(alpha):
            pixelResponses[alpha*i + j] = responses[j]

        # print(pixelResponses[alpha*i : alpha*(i+1)])
        # print(responses.shape)

        # ----------------------------------------------

    dictionary = KMeans(n_clusters=K, random_state=0, algorithm='elkan').fit(pixelResponses).cluster_centers_
    return dictionary
