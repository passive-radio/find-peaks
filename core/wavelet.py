import os
from swan import pycwt
import numpy as np
import matplotlib.pyplot as plt
from to_np_data import read_file

x_dir_path = "../../data/atom_linear_spectrum/"
filelist = os.listdir(x_dir_path)
filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][15:]))

for file in filelist:

    data = read_file(x_dir_path+file, ",", None, 640, errors="ignore", contains_x_axis=True)
    data.x = data.x.astype(np.int32)
    data.y = data.y.astype(np.float32)
    y = data.y

    # データのパラメータ
    N=len(y)
    dt = 1          # サンプリング間隔
    t = np.arange(0, N*dt, dt)
    # 高速フーリエ変換
    F = np.fft.fft(y)
    # 振幅スペクトルを計算
    freq = np.fft.fftfreq(N, d=dt)
    Amp = np.abs(F/(N/2))

    # x = np.arange(0, 20, 0.01)
    # y = np.sin(2 * np.pi * 1 * x) * 2 + np.sin(2 * np.pi * 2 * x) * 2  + np.cos(2 * np.pi * 10 * x)   



    Fs = 1
    omega0 = 8
    sigma = 10
    # (1)　Freqを指定してcwt
    freqs = freq[np.where(freq > 0)]
    
    mother_func = pycwt.Mexican_hat(sigma=sigma)
    r=pycwt.cwt_f(y,freqs,Fs,mother_func)
    rr=np.abs(r)

    plt.rcParams['figure.figsize'] = (12, 6)
    fig = plt.figure()
    ax1 = fig.add_axes([0.1, 0.75, 0.7, 0.2])
    ax2 = fig.add_axes([0.1, 0.1, 0.7, 0.60], sharex=ax1)
    ax3 = fig.add_axes([0.83, 0.1, 0.03, 0.6])

    ax1.plot(t, y, 'k')

    img = ax2.imshow(np.flipud(rr), extent=[0, N, 0, np.max(freq)],
                    aspect='auto', interpolation='nearest')

    fig.colorbar(img, cax=ax3)

    plt.show()