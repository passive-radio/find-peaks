import numpy as np
import matplotlib.pyplot as plt
from to_np_data import read_file

basepath = "../../data/atom_linear_spectrum/"
filename = "spectrum_type0_1.csv"

data = read_file(basepath+filename, ",", 0, 640, errors="ignore", contains_x_axis=True)
spectrum = data.y.values.astype(np.float32)

# データのパラメータ
N=len(spectrum)
dt = 1          # サンプリング間隔
t = np.arange(0, N*dt, dt)
# 高速フーリエ変換
F = np.fft.fft(spectrum)
# 振幅スペクトルを計算
freq = np.fft.fftfreq(N, d=dt)
Amp = np.abs(F/(N/2))

# グラフ表示
plt.figure()
plt.rcParams['font.family'] = 'Times New Roman'
plt.rcParams['font.size'] = 17
plt.subplot(121)
plt.plot(t, spectrum, label='f(n)')
plt.xlabel("Time", fontsize=20)
plt.ylabel("Signal", fontsize=20)
plt.grid()
leg = plt.legend(loc=1, fontsize=25)
leg.get_frame().set_alpha(1)
plt.subplot(122)
plt.plot(freq[1:int(N/2)], Amp[1:int(N/2)], label='|F(k)|')
plt.xlabel('Frequency', fontsize=20)
plt.ylabel('Amplitude', fontsize=20)
plt.grid()
leg = plt.legend(loc=1, fontsize=25)
leg.get_frame().set_alpha(1)
plt.show()