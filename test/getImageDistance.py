import numpy as np
from utils import chi2dist

def get_image_distance(hist1, histSet, method):

    # -----fill in your implementation here --------
    # def euclideanDist(H1, H2): 
    #     # return np.sqrt(np.sum((H1 - H2)**2))
    #     return np.linalg.norm(H1-H2)
    
    def chiDist(X, Yset):
        s = X + Yset
        d = Yset - X
        d = np.sum((d ** 2 / (s + 1e-10)), axis=1) / 2.0
        return d
    
    dist = np.zeros(len(histSet))
    hist1 = np.transpose(hist1) #fit the correct shape

    if (method == "euclidean"):
        dist = np.linalg.norm(histSet - hist1, axis=1) 
    else:
        dist = chiDist(hist1, histSet)

    # ----------------------------------------------

    return dist
