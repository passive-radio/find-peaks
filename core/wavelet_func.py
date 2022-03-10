import numpy as np
import matplotlib.pyplot as plt
import math
from to_np_data import read_file 

width = 6

# マザーウェーブレット：モルレーウェーブレット
def morlet(x, f, width):
    sf = f / width
    st = 1 / (2 * math.pi * sf)
    A = 1 / (st * math.sqrt(2 * math.pi))
    h = -np.power(x, 2) / (2 * st**2)
    co1 = 1j * 2 * math.pi * f * x
    return A * np.exp(co1) * np.exp(h)
 
# 連続ウェーブレット変換
def mycwt(Fs, data, fmax, wavelet_R=2):
    # Fs:           サンプリング周波数
    # data:         信号
    # wavelet_R:    マザーウェーブレットの長さ(秒)
    # fmax:         解析する最大周波数
 
    Ts = 1 / Fs     # サンプリング時間幅
    data_length = len(data) # 信号のサンプル数を取得
    
    # マザーウェーブレットの範囲
    wavelet_length = np.arange(-wavelet_R, wavelet_R, Ts)
 
    # 連続ウェーブレット変換後のデータを格納する配列の作成
    wn = np.zeros([fmax, data_length])
 
    # 連続ウェーブレット変換の実行
    for i in range(0, fmax):
        wn[i,:] = np.abs(np.convolve(data, morlet(wavelet_length, i+1, width), mode='same'))
        wn[i,:] = (2 * wn[i, :] / Fs)**2
    
    return wn
 
# 連続ウェーブレット変換後のカラーマップ作成関数
def cwt_plot(CWT, sample_time, fmax, fig_title):
    plt.imshow(CWT, cmap='jet', aspect='auto',vmax=abs(CWT).max(), vmin=-abs(CWT).max())  
    plt.title(fig_title)
    plt.xlabel("time[ms]")
    plt.ylabel("frequency[Hz]")
    plt.axis([0, len(sample_time), 0, fmax-1])
    plt.colorbar()

# plt.rcParams['figure.figsize'] = (16, 6)
# fig = plt.figure()
# ax1 = fig.add_axes([0.1, 0.75, 0.7, 0.2])
# ax2 = fig.add_axes([0.1, 0.1, 0.7, 0.60], sharex=ax1)
# ax3 = fig.add_axes([0.83, 0.1, 0.03, 0.6])

# ax1.plot(t, y, 'k')

# img = ax2.imshow(np.flipud(rr), extent=[0, N, 0, np.max(freq)],
#                  aspect='auto', interpolation='nearest')

# fig.colorbar(img, cax=ax3)

# plt.show()

if __name__ == "__main__":
    # 信号作成 ----------------------------------------
    Fs = 1000 # サンプリング周波数
    Ts = 1 / Fs # 1ステップあたりの時間幅
    time_S = 5 # 信号は5秒分
    t_data = np.arange(0,time_S, Ts) # 5秒分の時間配列
    
    basepath = "../../data/atom_linear_spectrum/"
    filename = "spectrum_type0_1.csv"

    data = read_file(basepath+filename, ",", 0, 640, errors="ignore", contains_x_axis=True)
    data.x = data.x.astype(np.int32)
    data.y = data.y.astype(np.float32)
    signal = data.y
    
    # データのパラメータ
    N=len(signal)
    dt = 1          # サンプリング間隔
    t = np.arange(0, N*dt, dt)
    # 高速フーリエ変換
    # F = np.fft.fft(signal)
    # 振幅スペクトルを計算
    # freq = np.fft.fftfreq(N, d=dt)
    # Amp = np.abs(F/(N/2))
    freqs = np.fft.fftfreq(N, d=dt)
    Fs = 1/0.01
    omega0 = 8
    # (1)　Freqを指定してcwt
    freqs = freqs[np.where(freqs > 0)]
        
    # 連続ウェーブレット変換 ----------------------------------------
    fmax=np.max(freqs) # 解析する最大周波数
    cwt_signal01 = mycwt(Fs=Fs, data=signal, fmax=fmax)
 
    # 以下、図用 ----------------------------------------
    plt.figure(0) # signal01を連続ウェーブレット変換した時のカラーマップの図
    fig_title01 = "cwt signal01"
    cwt_plot(cwt_signal01, t, fmax, fig_title01)
    
    plt.show()