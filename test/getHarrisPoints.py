import numpy as np
import cv2 as cv
from scipy import ndimage, signal
from utils import imfilter


def get_harris_points(I, alpha, k):
    #convert to greyscale
    if len(I.shape) == 3 and I.shape[2] == 3:
        I = cv.cvtColor(I, cv.COLOR_RGB2GRAY)
    if I.max() > 1.0:
        I = I / 255.0

    # -----fill in your implementation here --------
    #precompute gradients
    #axis=0 => along y axis = x gradients
    Ix = ndimage.sobel(I, axis=0) 
    Iy = ndimage.sobel(I, axis=1) 
    Ixx = Ix * Ix 
    Ixy = Ix * Iy 
    Iyx = Iy * Ix
    Iyy = Iy * Iy

    p = 3
    sumFilter = np.ones((p,p))
    Sxx = signal.convolve2d(Ixx, sumFilter, mode="same")
    Sxy = signal.convolve2d(Ixy, sumFilter, mode="same")
    Syx = signal.convolve2d(Iyx, sumFilter, mode="same")
    Syy = signal.convolve2d(Iyy, sumFilter, mode="same")

    R = (Sxx * Syy - Sxy * Syx) - k * (Sxx + Syy)**2
    R = R.reshape((len(I), len(I[0])))

    #get indices of top largest ones
    topIndices = np.argpartition(R, -alpha, axis=None)[-alpha:] #flatten array before sorting to find in both dimensions
    # get the original x,y indices from the "flattened" indices
    points = [(int(topIndices[i] / len(I[0])), topIndices[i] % len(I[0])) for i in range(alpha)]
    
    # cv.imshow('test.png', Iyx.astype(np.uint8))
    # cv.waitKey(0)
    # ----------------------------------------------
    
    return points

