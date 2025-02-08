import cv2 as cv
import numpy as np
from RGB2Lab import rgb2lab
from utils import *

#I = image
#filterBank = list of 20 different filters
#including gaussian, laplacian of gaussian, x and y gradient of gaussians
#each at 5 different scales
def extract_filter_responses(I, filterBank):
    #will change if black and white image
    length = len(I)
    width = len(I[0])

    I = I.astype(np.float64)
    if len(I.shape) == 2:
        I = np.tile(I, (3, 1, 1))

    # -----fill in your implementation here --------
    #convert color space of I from RGB to Lab  
    if (len(I) == 3):
        Im = I
    else: 
        Im = rgb2lab(I)  
    filterResponses = np.zeros((length, width, 3 * len(filterBank)))

    #apply filter to each color channel of I2
    if len(I) == 3: #black and white
        for i in range (len(filterBank)): #step by 3 every time
            filterResponses[:,:,3*i] = imfilter(Im[0,:,:], filterBank[i])
            filterResponses[:,:,3*i+1] = imfilter(Im[1,:,:], filterBank[i])
            filterResponses[:,:,3*i+2] = imfilter(Im[2,:,:], filterBank[i])
    else: 
        for i in range (len(filterBank)): #step by 3 every time
            filterResponses[:,:,3*i] = imfilter(Im[:,:,0], filterBank[i])
            filterResponses[:,:,3*i+1] = imfilter(Im[:,:,1], filterBank[i])
            filterResponses[:,:,3*i+2] = imfilter(Im[:,:,2], filterBank[i])
    
    # Normalize each filter response to be in the range [0, 255]
    min_vals = filterResponses.min(axis=(0, 1), keepdims=True)
    max_vals = filterResponses.max(axis=(0, 1), keepdims=True)

    # Avoid division by zero
    range_vals = np.maximum(max_vals - min_vals, 1e-5)
    normalized = (filterResponses - min_vals) / range_vals
    filterResponses = normalized * 255
    # ----------------------------------------------
    
    return filterResponses
