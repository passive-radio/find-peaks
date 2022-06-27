import time
import json
import sys

import scipy.signal
import numpy as np
from numpy.random import PCG64

from .Module.module import Generator
from .Module.functions import gauss, butterworth_filter, chebyshev_filter

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
        self.length = length
        self.peak_pos = []
        pass
    
    def add_peaks(self, pos, amp, sigma, label_ci:float = 2):
        
        if len(pos) != len(amp) or len(pos) != len(sigma) or len(amp) != len(sigma):
            raise
            
        pos = super().relocated_peaks(pos, sigma)
        for i in range(len(pos)):
            # print(amp[i], np.max(self.add_peak(pos[i], amp[i], sigma[i])))
            self.signal = self.signal + self.add_peak(pos[i], amp[i], sigma[i])
            
            if 3 < label_ci:
                label_ci = 3
                
            start = int(pos[i] - sigma[i]*label_ci)
            end = int(pos[i] + sigma[i]*label_ci)
            if start < 0:
                start = 0
            elif self.length - 2 < end:
                end = int(self.length - 1)
            self.peak_pos.append([start, int(pos[i]), end])
        
        self.peak_num = len(pos)
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
        return butterworth_filter(signal_val, sampling_rate, fp, fs, gpass, gstop)
    
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
        peak_value = gauss(np.arange(0, self.length, 1), pos, amp, sigma)
        # self.signal = self.signal + peak_value
        return peak_value
    
    @property
    def get_signal(self):
        return self.signal
    @property
    def get_baseline(self):
        return self.baseline
    @property
    def get_peak_pos(self):
        return self.peak_pos
    @property
    def get_peak_num(self):
        return self.peak_num
    
    def init(self):
        self.signal = np.zeros(self.length)
        self.baseline = np.zeros(self.length)
        self.peak_num = None
        self.peak_pos = []
        
class signal_chebyshev_smooothed_baseline(signal_butterworth_smooothed_baseline):
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
        self.length = length
        self.peak_pos = []
        pass
    
    def add_filter(self, signal_data, sampling_rate, fp, fs, gpass, gstop):
        return chebyshev_filter(signal_data, sampling_rate, fp, fs, gpass, gstop)