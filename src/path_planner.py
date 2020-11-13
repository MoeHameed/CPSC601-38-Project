import utils
import numpy as np

# Given start and end cell, return shortest list of cells
def genInitialPath(start, end):
    return [start, end]

def a_star_search(start, end):
    toSearch = [start]
    currCell = start
    path = []

    while len(toSearch) > 0:
        if np.array_equal(currCell, end):
            return path

        

    return None
    

#print(a_star_search([0, 0], [10, 10]))
