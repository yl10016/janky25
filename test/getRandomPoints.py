import numpy as np


def get_random_points(I, alpha):

    # -----fill in your implementation here --------
    points = np.zeros((alpha, 2))

    # points = np.array([np.random.choice(len(I), size=alpha, replace=False), 
    #                    np.random.choice(len(I[1]), size=alpha, replace=False)])
    
    #generate range
    potentialX = np.arange(stop=len(I))
    potentialY = np.arange(stop=len(I[0]))

    #get cartesian product of all types
    possibleCombos = [(x,y) for x in potentialX for y in potentialY]

    #choose random indices
    randomIndices = np.random.choice(len(possibleCombos), size=alpha, replace=False)

    #populate points with (x,y) pairs
    points = np.array([possibleCombos[i] for i in randomIndices])
    # ----------------------------------------------

    return points
