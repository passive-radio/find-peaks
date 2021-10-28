from configparser import BasicInterpolation
from os import name, read, sep

import matplotlib.pyplot as plt
import matplotlib.cm as cm
import pandas as pd
from pandas.io.clipboards import read_clipboard
from scipy.optimize import curve_fit
import numpy as np
from pprint import pprint
import csv

from findPeaks import findPeaks, read_data, reset_range

def main():
    base_url = "data_spectrum/"
    endpoint = "sample01.asc"
    
    data = read_data(base_url + endpoint, 3, ',')
    data = reset_range(data, 1600)
    findpeaks = findPeaks(data)
    
    #初期値のリストを作成
    #[amp,ctr,wid]
    guess = []
    guess.append([350, 3000, 10])
    guess.append([250, 3400, 10])

    #バックグラウンドの初期値
    background = 0

    #初期値リストの結合
    guess_total = []
    for i in guess:
        guess_total.extend(i)
    guess_total.append(background)
    
    popt, pcov = findpeaks.exp_func_fit(*guess_total, mode="g")
    findpeaks.fit_plot(*popt, func="exp")
    
    print(findpeaks.peakxs)
    print(findpeaks.peakwidth)
        
    plt.show()
    
if __name__ == "__main__":
    main()