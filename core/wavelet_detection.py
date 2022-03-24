import os
import sys
from unittest import result

import scipy.signal
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

sys.path.append('utils/')
sys.path.append('../')

from to_np_data import read_file
from utils.dataset import load_data
import mother_func as mother


def to_wavelet_by_morlet(signal,Fs, freqs, wavelet_span, width, convolve_mode="same"):
    """
    離散ウェーブレット変換後のデータを格納する配列の作成
    """
    Ts = 1/Fs
    wavelet_length = np.arange(-wavelet_span, wavelet_span, Ts)
    wn = np.zeros([len(freqs), len(signal)])
    freqs = np.sort(freqs)
    length = len(freqs)
    for i, freq in enumerate(freqs):
        wn[length-1-i,:] = np.abs(np.convolve(signal, mother.morlet_func(wavelet_length, freq, width), mode=convolve_mode))
        wn[length-1-i,:] = (2 * wn[length-1-i, :] / Fs)**2
    
    return wn

# 連続ウェーブレット変換
def to_cwt(signal, Fs: int, dt=1, wavelet_span=2, fmax=None, mother_func="morlet",
            width=6, c_mode="same"):
    """
    ## Func to run cwt
    
    ## Parameters
    - Fs:           サンプリング周波数
    - dt:           サンプリング間隔(time)
    -  data:         信号
    - wavelet_span:    マザーウェーブレットの長さ(秒)
    - fmax:         解析する最大周波数
    """
    
    N=len(signal)
    dt = dt          # サンプリング間隔
    freqs = np.fft.fftfreq(N, d=dt)
    freqs = freqs[np.where(freqs > 0)]
    if mother_func == "morlet":
        np_arr_wavelet = to_wavelet_by_morlet(signal, Fs, freqs, wavelet_span, width, c_mode)
    elif mother_func == "mexican_hat":
        return
    
    return np_arr_wavelet
    

def plt_scalogram(signal, dt, np_result, peak_prob):
    
    N = len(signal)
    t = np.arange(0, N*dt, dt)
    try:
        fmax = np.max(signal)
    except:
        signal = signal.values
        fmax = np.max(signal)
    
    plt.rcParams['figure.figsize'] = (12, 6)
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.75, 0.7, 0.2])
    ax2 = fig.add_axes([0.1, 0.1, 0.7, 0.60], sharex=ax1)
    ax3 = fig.add_axes([0.83, 0.1, 0.03, 0.6])

    ax1.plot(t, signal, 'k')
    ax1.plot(peak_prob, signal[peak_prob], "x")

    img = ax2.imshow(np.flipud(np_result), extent=[0, N, 0, fmax],
                        aspect='auto', interpolation='nearest')

    fig.colorbar(img, cax=ax3)
    plt.show()
    
def predict_pos(np_wavelet, c:float, Fs:float):
    np_sum = np.sum(np_wavelet, axis=0)
    prob = softmax(np_sum, c, Fs)
    return prob

def softmax(data, c:float, Fs):
    num = np.exp(c*data)
    den = np.sum(num)
    return num/den

def moving_average(data, distance):
    distance=int(distance)
    data = pd.Series(data)
    if distance % 2:
        backward_ma =data.rolling(window=distance).mean()
        centered_ma = backward_ma.shift(-int(distance/2)).rolling(window=int(distance/2)).mean()
    
    else:
        centered_ma = data.rolling(window=distance, center=True).mean()
        
    centered_ma[0:distance+1] = data.rolling(window=distance, center=False).mean().shift(-distance)[0:distance+1]
    centered_ma[len(data)-1-distance:len(data)] = data.rolling(window=distance).mean().shift(distance)[len(data)-1-distance:len(data)]
    
    return centered_ma.to_numpy()

def to_scalogram(filepath, sep=",", headers=None, footers=None, errors="ignore", 
                    contains_x_axis=True, width=6, wavelet_span=2, Fs=100, soft_max_c=1):
    if os.path.splitext(filepath)[1] == ".npz":
        signal, label = load_data(filepath)
    else:
        data = read_file(filepath, sep, headers, footers, errors, contains_x_axis)
        signal = data.y.astype(np.float64)
    dt = 1          # サンプリング間隔
    convolve_mode = "same"
    
    # 連続ウェーブレット変換 ----------------------------------------
    result_wavelet = to_cwt(signal, Fs, dt, wavelet_span, mother_func="morlet", 
                            width=width, c_mode = convolve_mode)
    prob = predict_pos(result_wavelet, soft_max_c, Fs)
    prob_ma = moving_average(prob, distance=len(prob)/4)
    prob_avg = np.average(prob)
    
    peak_prob= []
    for i, p in enumerate(prob):
        if p > prob_ma[i] and p > prob_avg:
            peak_prob.append(i)
    peak_prob = np.array(peak_prob)
    
    # peak_pos_scipy, _ = scipy.signal.find_peaks(prob, distance=len(prob)/10)
    # for pos in peak_pos_scipy:
    #     if prob[pos] > prob_ma[pos] and prob[pos] > prob_avg:
    #         print(pos, prob[pos])
    plt_scalogram(signal, dt, result_wavelet, peak_prob)

def to_scalogram_dir(dir_path, sep=",", headers=None, footers=None, errors="ignore", 
                    contains_x_axis=True, width=6, wavelet_span=2, Fs=100, soft_max_c=1, num_sort_pos:int=6):
    filelist = os.listdir(dir_path)
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][num_sort_pos:]))
    for file in filelist:
        to_scalogram(dir_path+file, sep, headers, footers, errors,
                        contains_x_axis,width, wavelet_span, Fs, soft_max_c)
if __name__ == "__main__":
    
    base_path = "../../data/atom_linear_spectrum/"
    to_scalogram_dir(base_path, ",", 0, 640, width=0.4, wavelet_span=4, Fs=10, soft_max_c=1e-8)
    # base_path = "../../data/gamma_ray/"
    # to_scalogram_dir(base_path, ",", 0, 4096, width=2, wavelet_span=10, Fs=2, soft_max_c=1e-10)
    # base_path = "../../data/proportional_tubes_x_ray/"
    # to_scalogram_dir(base_path, ",", 11, 1036, width=2, wavelet_span=6, Fs=2, soft_max_c=1e-10)
    
    # filepath = "../sample_data/sample_data.csv"
    # to_scalogram(filepath, ",", 0,640,width=1, wavelet_span=1, Fs=10, soft_max_c=10e-8)