import time
import scipy.signal
import numpy as np
from numpy.random import PCG64
from module.module import Generator
from module.functions import gauss

class signal_butterworth_smooothed_baseline(Generator):
    '''
    # signal generator using butterwoth filter as the noise smoother
    
    ## Process
    1. add baseline
        1. add noise signal
        1. smooth the noise signal by lowpassfilter(for here, it's butterworth filter)
    1. add peaks
    1. add noise
    '''
    
    def __init__(self, length:int=None) -> None:
        self.rnd_gen = np.random.Generator(PCG64(int(time.time())))
        self.signal = np.zeros(length)
        self.baseline = None
        pass
    
    def add_peaks(self, pos, amp, sigma):
        
        if len(pos) != len(amp) or len(pos) != len(sigma) or len(amp) != len(sigma):
            raise
            
        pos = super().relocated_peaks(pos, sigma)
        for i in range(len(pos)):
            self.signal = self.signal + self.add_peak(pos[i], amp[i], sigma[i])
        
        return self
    
    def add_baseline(self, length:int, height:float, std:float, sp, fp, fs, gpass, gstop):
        baseline = self.rnd_gen.normal(height, std, (length))
        baseline = self.add_filter(baseline, sp, fp, fs, gpass, gstop)
        self.baseline = baseline
        self.signal = baseline
        return self
    
    def add_filter(self, signal_val, sampling_rate, fp, fs, gpass, gstop):
        """
        ## Butterworth filter (lowpass filter) fuction
        
        ## Parameters
            - signal_val: signal
            - sampling_rate: 波形のサンプリングレート
            - fp: 通過域端周波数[Hz]
            - fs: 阻止域端周波数[Hz]
            - gpass: 通過域端最大損失[dB] passband ripple 
            - gstop: 阻止域端最小損失[dB] stopband attenuation
            - curve: 減衰関数  
                - linear: 線形減衰
        """
        gpass *= -1
        gstop *= -1
        sampling_time = len(signal_val)          #サンプリング時間: スペクトルデータの時間    
        fn = sampling_rate / 2                        #ナイキスト周波数
        wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
        ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
        N, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
        
        # w = fp / fn # Normalize the frequency
        # b, a = signal.butter(5, w, 'low')
        # if N < 0:
        #     N = 0
        b, a = scipy.signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算
        # if a.any()<2:
        #     a=2
        # if type(a) == int or len(a) < 2:
        #     a_temp = copy.copy(a)
        #     a = np.zeros((2))
        #     a[0:2] = a_temp
        filtered = scipy.signal.filtfilt(b, a, signal_val)                  #信号に対してフィルタをかける
        return filtered                                      #フィルタ後の信号を返す
    
    def add_noise(self, signal:np.ndarray = None, length:int = None, max_height:float = None, stn: float = None, sigma:float = 1.0):
        
        if signal is not None:
            length = len(signal)
        if signal is None and length is None:
            length = len(self.signal)
        
        if stn is not None and signal is not None:
            max_height = np.max(signal) * stn
        
        if max_height is not None:
            noise = self.rnd_gen.normal(0, sigma, length)
            noise_max = np.max(noise) if np.max(noise) > np.abs(np.min(noise)) else np.abs(np.min(noise))
            noise = (noise + noise_max) * max_height / noise_max / 2
            self.signal = self.signal + noise

        if stn is not None:
            length = len(self.signal)
            noise = self.rnd_gen.normal(0, sigma, length)
            signal_max = np.max(self.signal)
            noise_max = np.max(noise) if np.max(noise) > np.abs(np.min(noise)) else np.abs(np.min(noise))
            noise_min = np.min(noise)
            noise = (noise - noise_min) * signal_max / (noise_max * stn * 2)
            self.signal = self.signal + noise
            
        return self
    
    def add_peak(self, pos, amp, sigma):
        width = len(self.signal)
        peak_value = gauss(np.arange(0, width), pos, amp, sigma)
        self.signal = self.signal + peak_value
        return peak_value
    
    @property
    def get_signal(self):
        return self.signal
    @property
    def get_baseline(self):
        return self.baseline

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    
    fig, axs = plt.subplots(2, 1, figsize=(10,6))
    
    signal = signal_butterworth_smooothed_baseline(length=1000)
    
    signal = signal.add_baseline(1000, 10, 0.1, 0.4, 4e-4, 4e-2, -0.5, -10)
    signal_val = signal.get_signal
    axs[0].plot(signal_val)
    
    amp = [2, 2]
    pos = [400, 360]
    sigma = [10, 10]
    signal = signal.add_peaks(pos, amp, sigma)
    signal = signal.add_noise(stn=20)
    signal_val = signal.get_signal
    axs[1].plot(signal_val)
    
    plt.show()