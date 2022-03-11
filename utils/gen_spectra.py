import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
import time
"""
# The module to generate a set of simulated spectrum data

here, spectrum data contains  
- baseline
- noise
- peaks

"""


#バターワースフィルタ（ローパス）
def lowpass(x, samplerate, fp, fs, gpass, gstop):
    """
    ## Parameters
    - samplerate = 10 #波形のサンプリングレート
    - fp = 3000       #通過域端周波数[Hz]
    - fs = 6000       #阻止域端周波数[Hz]
    - gpass = 3       #通過域端最大損失[dB]
    - gstop = 40      #阻止域端最小損失[dB]
    """
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す

def baseline(width, baseline_height, std):
    np_rand = np.random.normal(baseline_height, std, (width))
    np_lowpassed = lowpass(np_rand,40, 1, 2, 3, 40)
    return np_lowpassed

def add_noise(signal, noise_scale):
    np_noise = np.random.normal(0, noise_scale, (len(signal)))
    return signal+np_noise

def gauss(x, a=1, mu=0, sigma=1):
    return a * np.exp(-(x - mu)**2 / (2*sigma**2))

def add_peak(signal, pos, scale, a=1, mu=0, sigma=1):
    peak = gauss(np.arange(0,scale,1), a, mu, sigma)
    signal[pos:pos+scale] = signal[pos:pos+scale] +peak
    return signal

def gen_sim_signal(width, baseline_height, baseline_std, peak_pos,
                    peak_scale, gauss_a, gauss_mu, gauss_sigma, noise_scale):
    np.random.seed(int(time.time()))
    signal = baseline(width, baseline_height, baseline_std)
    signal = add_peak(signal, peak_pos, peak_scale, gauss_a, gauss_mu, gauss_sigma)
    signal = add_noise(signal, noise_scale)
    return signal

if __name__ == "__main__":
    width = 2000
    np_lowpassed = baseline(width, 400, 10, 2)
    signal = add_peak(np_lowpassed, pos=400, scale=200, a=50, mu=0, sigma=20)
    signal = add_noise(signal, noise_scale=2)
    plt.plot(range(0, width, 1), np_lowpassed, "gray")
    plt.plot(range(0, width, 1), signal, "orange")
    
    plt.show()
