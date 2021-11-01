import matplotlib.pyplot as plt
from pprint import pprint
import numpy as np

import pandas as pd

from findPeaks import findPeaks, read_data, reset_range

def main():
    base_url = "data_spectrum/"
    endpoint = "sample01.asc"
    
    data_origin = read_data(base_url + endpoint, 3, ',')
    data = reset_range(data_origin, 1600)
    findpeaks = findPeaks(data)
    
    #初期値のリストを作成
    #[amp,ctr,wid]
    guess = []
    guess.append([3000, 350, 10])
    guess.append([3400, 250, 10])

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
    
    # data = reset_range(data_origin, 2830, 3240)
    # findpeaks = findPeaks(data)
    
    # data = [[0, 100],[3, 10], [6, 0], [10, 20], [12, 80]]
    # data = pd.DataFrame(data, columns=["x", "y"])
    # findpeaks=findPeaks(data)
    
    test_params = [3000, 0.1, 3400, 0.1, 0]
    popt,pcov = findpeaks.plynomi_func_fit(*test_params, deg=3, mode="g")
    print(popt)
    findpeaks.fit_plot(*popt, func="poly", deg=3)
    # np.set_printoptions(threshold=np.inf)
    # print(popt)
    plt.show()
    
    
if __name__ == "__main__":
    main()