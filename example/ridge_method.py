"""
[Under development] Ridge method

more detailed info about the method coded here:
see https://doi.org/10.1063/1.3505103

mother function: morlet function
"""
import math
from operator import index
import numpy as np
import matplotlib.pyplot as plt
from utils.dataset import load_data
from core.wavelet_detection import wavelet_transform, plt_scalogram
from tqdm import tqdm
from core.mother_func import mother_wavelet
import scipy.signal


def main2():
    signal, label = load_data(filepath="../data/dataset/4/signal0.npz")

    a_wav_scale = 100
    deltab = 1
    Fs = 0.1
    mother_func = "LoG"
    mother_func_width = 200

    mothers = mother_wavelet(a_wav_scale, deltab, mother_func_width)
    log_func = mothers.mother_func("LoG", 1)
    mothers.plot_mother

    scalogram = wavelet_transform(signal, a_wav_scale, deltab, Fs, 
                                    mother_func_width, "LoG")
    freqs = np.fft.fftfreq(len(signal), 1/deltab)
    freqs = np.sort(freqs[np.where(freqs > 0)])

    plt_scalogram(signal, deltab, scalogram, freqs=freqs)

def ridge_n_peak(a_max, a_min, a_num, deltab, width_method="res_a", a_space="log10"):
    
    signal,_ = load_data(filepath="../data/dataset/4/signal0.npz")
    
    if a_space == "log10":
        pow_max = np.log10(a_max)
        pow_min = np.log10(a_min)

    Fs = 0.1
    a_array = np.logspace(pow_max, pow_min, a_num, base=10)
    init_ridges = []
    ridges = []
    for i,a in enumerate(a_array):
        width = a*2
        # b_space = np.arange(-width.astype(uint32)+deltab/2, width.astype(uint32)+deltab/2, deltab)
        scalogram = wavelet_transform(signal, a, deltab, Fs, width, "LoG")
        tab = scalogram.sum(axis=0)
        tab_avg = np.average(tab)
        plt.plot(tab)
        plt.show()
        
        indexes, _ = scipy.signal.find_peaks(tab, height=tab_avg, distance=width)
        print('Peaks are: %s' % (indexes))
        
        ridges_arr = []
        index_temp = []
        ridge_id = []
        
        if i == 1:
            for j, index in enumerate(indexes):
                ridges.append(np.array(index))

        else: 
            for j, index in enumerate(indexes):
                for k, ridge in enumerate(ridges):
                    
                    if (ridge - index).any() < deltab*10:
                        ridges_arr.append(k)
                        index_temp.append(j)
                        ridge_id.append(np.where(ridge-index < deltab*10))
                        print(j, k, np.where(ridge-index < deltab*10))
                    else:
                        ridges.append(np.array(index))
                if len(ridges) <= j:
                    """
                    条件に当てはまればridge[i]にappend する
                    """
            ridges_arr = np.array(ridges_arr)
            print(np.unique(ridges_arr))
            
        if i == 1:
            init_ridges = indexes


# fig, axs = plt.subplots(3, 1, figsize=(6,6))
# axs[0].plot(wab, label="W(a,b)")
# axs[0].legend()
# axs[1].plot(signal, label=f"signal upsample by factor {1/deltab}")
# axs[1].legend()
# axs[2].plot(tab, label="T(a,b)")
# axs[2].legend()
# plt.show()

if __name__ == "__main__":
    
    ridge_n_peak(200, 5, 10, 1)