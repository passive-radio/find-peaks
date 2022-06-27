"""
scraps of functions expected to be used more than once or useful in the future dev
"""

from signal import signal


def gauss(x, pos, amp=1, sigma=1):
    from numpy import exp
    
    val = amp * exp(-(x - pos)**2 / (2*sigma**2))
    return val

def butterworth_filter(signal_data, sampling_rate, fp, fs, gpass, gstop):
    """
    ## Butterworth filter (lowpass filter) fuction
    
    ## Parameters
        - signal_val: signal(sequence)
        - sampling_rate: 波形のサンプリングレート
        - fp: 通過域端周波数[Hz]
        - fs: 阻止域端周波数[Hz]
        - gpass: 通過域端最大損失[dB] passband ripple 
        - gstop: 阻止域端最小損失[dB] stopband attenuation
        - curve: 減衰関数  
            - linear: 線形減衰
    """
    import scipy.signal
    
    gpass *= -1
    gstop *= -1
    fn = sampling_rate / 2                        #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = scipy.signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    
    b, a = scipy.signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算

    filtered = scipy.signal.filtfilt(b, a, signal_data)                  #信号に対してフィルタをかける
    return filtered                                      #フィルタ後の信号を返す

def chebyshev_filter(signal_data, sampling_rate, fp, fs, gpass, gstop):
    """
    ## Chebysheb filter (lowpass filter) fuction
    
    ## Parameters
        - signal_data: signal(sequence)
        - sampling_rate: 波形のサンプリングレート
        - fp: 通過域端周波数[Hz]
        - fs: 阻止域端周波数[Hz]
        - gpass: 通過域端最大損失[dB] passband ripple 
        - gstop: 阻止域端最小損失[dB] stopband attenuation
        - curve: 減衰関数  
            - linear: 線形減衰
    """
    
    import scipy.signal
    
    fn = sampling_rate / 2
    wp = fp / fn
    ws = fs / fn
    N, Wn = scipy.signal.cheb1ord(wp, ws, gpass, gstop, False)
    b, a = scipy.signal.cheby1(N, 3, Wn, "low", False)
    filtered = scipy.signal.filtfilt(b, a, signal_data)
    return filtered