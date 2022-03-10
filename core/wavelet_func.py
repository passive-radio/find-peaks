import os

import numpy as np
import matplotlib.pyplot as plt

from to_np_data import read_file
import mother_func as mother


def to_wavelet_by_morlet(signal,Fs, freqs, wavelet_span, width, convolve_mode="same"):
    """
    連続ウェーブレット変換後のデータを格納する配列の作成
    """
    Ts = 1/Fs
    wavelet_length = np.arange(-wavelet_span, wavelet_span, Ts)
    wn = np.zeros([len(freqs), len(signal)])
    freqs = np.sort(freqs)
    print(freqs)
    length = len(freqs)
    for i in range(len(freqs)):
        wn[length-1-i,:] = np.abs(np.convolve(signal, mother.morlet_func(wavelet_length, i+1, width), mode=convolve_mode))
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
    

def show_result(signal, dt, np_result):
    
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

    img = ax2.imshow(np.flipud(np_result), extent=[0, N, 0, fmax],
                        aspect='auto', interpolation='nearest')

    fig.colorbar(img, cax=ax3)
    plt.show()
    
def check_wavelet_dir(dir_path, sep=",", headers=None, footers=None, errors="ignore", contains_x_axis=True):
    filelist = os.listdir(dir_path)
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][15:]))
    for file in filelist:
        data = read_file(dir_path+file, ",", headers, footers, errors=errors, contains_x_axis=contains_x_axis)
        signal = data.y.astype(np.float64)
        
        dt = 1          # サンプリング間隔
        Fs = 1/0.01
        wavelet_span = 2
        convolve_mode = "same"
        
        # 連続ウェーブレット変換 ----------------------------------------
        result_wavelet = to_cwt(signal, Fs, dt, wavelet_span, mother_func="morlet", 
                                width=6, c_mode = convolve_mode)
        show_result(signal, dt, result_wavelet)
if __name__ == "__main__":
    
    base_path = "../../data/atom_linear_spectrum/"
    filename = "spectrum_type0_1.csv"

    check_wavelet_dir(base_path, ",", 0, 640)