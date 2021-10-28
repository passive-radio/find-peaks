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
    endpoint = "SpeciesA_Isolate1-1_110131.txt"
    endpoint = "210625Co.asc"
    
        
    data = read_data(base_url + endpoint, 8, ',')
    data = pd.DataFrame(data, columns=['x', 'y'])
    data = reset_range(data, 1600)
    
    findpeaks = findPeaks(data)
    
    #初期値のリストを作成
    #[amp,ctr,wid]
    guess = []
    guess.append([350, 3000, 10])
    guess.append([250, 3400, 10])

    #バックグラウンドの初期値
    background = 5

    #初期値リストの結合
    guess_total = []
    for i in guess:
        guess_total.extend(i)
    guess_total.append(background)
    
    popt, pcov = curve_fit(findpeaks.exp_func, data.x, data.y, p0=guess_total)
    peak_x = [popt[i] for i in range(len(popt)) if i % 3 ==1]
    print(peak_x)
    
    fit = findpeaks.exp_func(*popt)
    plt.scatter(data.x, data.y, s=20)
    plt.plot(data.x, fit , ls='-', c='black', lw=1)
    
    y_list = findpeaks.exp_fit_plot(*popt)
    baseline = np.zeros_like(data.x) + popt[-1]
    for n,i in enumerate(y_list):
        plt.fill_between(data.x, i, baseline, facecolor=cm.rainbow(n/len(y_list)), alpha=0.6)
    
    plt.show()
    
if __name__ == "__main__":
    main()