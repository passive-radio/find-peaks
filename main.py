from configparser import BasicInterpolation
from os import read

import matplotlib.pyplot as plt
import pandas as pd
from pandas.core.algorithms import value_counts
from findPeaks import findPeaks

def main():
    base_url = "data_spectrum/"
    endpoint = "SpeciesA_Isolate1-1_110131.txt"
    
    data = pd.read_csv(base_url + endpoint, names=['x', 'y'], sep=" ")
    findpeaks = findPeaks(1, data)    
    data = findpeaks.reset_range([0,1000])
    plt.scatter(data.x, data.y, s=5)
    plt.show()

if __name__ == "__main__":
    main()