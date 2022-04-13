"""
# dataset  
provides

## spectrum data generation by following steps  
    - add baseline
    - smoothing by butterworth filter (high freq cut)
    - add peaks
    - add noise
"""

import os
import shutil
import json
import time
import math
import copy

from scipy import signal
import matplotlib.pyplot as plt
import numpy as np
from numpy import argmax
from tqdm import tqdm

#バターワースフィルタ（ローパス）
def add_butterworth_filter(x, sampling_rate, fp, fs, gpass, gstop):
    x=copy.copy(x)
    """
    ## Butterworth filter (lowpass filter) fuction
    
    ## Parameters
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
    sampling_time = len(x)          #サンプリング時間: スペクトルデータの時間    
    fn = sampling_rate / 2                        #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    
    # w = fp / fn # Normalize the frequency
    # b, a = signal.butter(5, w, 'low')
    # if N < 0:
    #     N = 0
    b, a = signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算
    # if a.any()<2:
    #     a=2
    # if type(a) == int or len(a) < 2:
    #     a_temp = copy.copy(a)
    #     a = np.zeros((2))
    #     a[0:2] = a_temp
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す

def add_baseline(width, baseline_height, std):
    baseline = np.random.normal(baseline_height, std, (width))
    # np_lowpassed = lowpass(np_rand,40, 1, 2, 3, 40)
    return baseline

def add_noise(baseline, signal, nsr):
    '''
    ## function which adds noise on signal
    
    ## Parameters
        - baseline: baseline sequence data
        - signal: signal sequence data
        - nsr: noise signal ratio (noise/signal)
    '''
    max_pos = argmax(signal,axis=0)
    signal_amp = signal[max_pos] - baseline[max_pos]
    noise_scale = nsr * signal_amp
    
    if noise_scale < 0:
        noise_scale = np.abs(noise_scale)
    
    try: 
        np_noise = np.random.normal(0, noise_scale, (len(signal)))
    except ValueError as e:
        np.random.seed(int(time.time()))
        np_noise = np.random.normal(0, noise_scale, (len(signal)))
    return signal+np_noise

def gauss(x, pos, amp=1, sigma=1):
    return amp * np.exp(-(x - pos)**2 / (2*sigma**2))

def add_peak(signal, raw_signal, label, pos, amp=1, sigma=1, label_ci=1):
    signal = copy.copy(signal)
    width = len(signal)
    height = np.max(raw_signal, axis=0).astype(np.float32)
    n_pos = int(pos * width)
    n_sigma = int(sigma*width)
    amp = height*amp
    n_scale = width
    peak = gauss(np.arange(0, n_scale, 1), n_pos, amp, n_sigma)
    signal += peak
    if label_ci > 3:
        label_ci = 3
    label[n_pos-n_sigma*label_ci: n_pos+n_sigma*label_ci] = 1
    return signal, label, raw_signal

def add_peaks(base_signal, pos_list, a_list, sigma_list, label_ci=1):
    """
    ## Function which adds the optional number of peaks on the base signal
    
    ## Parametes
        - base_signal: base signal
        - pos_list: list of the center positions of each peaks
        - a_list: list of the amplitudes of each peaks
        - sigma_list: list of the sigma(σ) of each peaks
        - label_ci: confidence interval (as peak bandwidth) => label data
    """
    signal = copy.copy(base_signal)
    raw_signal = signal
    pos_list = np.array(pos_list)
    a_list = np.array(a_list)
    sigma_list = np.array(sigma_list)
    label = np.zeros(len(signal))
    pos_list_original = copy.copy(pos_list)
    if 1 < len(pos_list):
        for i in range(len(pos_list)):
            for j in range(len(pos_list)):
                # print(pos_list[j] - sigma_list[j], pos_list[i], pos_list[j] + sigma_list[j])
                if i != j and pos_list[j]-sigma_list[j] < pos_list[i] < pos_list[j] + sigma_list[j]:
                    if pos_list[i] < pos_list[j]:
                        pos_list[i] = pos_list[j] - 40*sigma_list[j]
                    else:
                        pos_list[i] = pos_list[j] + 40*sigma_list[j]
                    if pos_list[i] < 0:
                        pos_list[i] = 0
                    elif pos_list[i] > 1:
                        pos_list[i] = 1
        # print(f"{pos_list_original} -> {pos_list}")
        if pos_list_original.all() != pos_list.all():
            print(f"{pos_list_original} -> {pos_list}")
    for i, _ in enumerate(pos_list):
        signal, label, raw_signal = add_peak(signal, raw_signal, label, pos_list[i], a_list[i], sigma_list[i], label_ci=label_ci)
    return signal, label, len(pos_list)

def gen_dataset(spectrum_num, width, dataset_dir, label_ci, baseline_height_range, std_range, 
                sprate_range, fp_range, fs_range, gpass_range, gstop_range, peak_num_range, pos_range,
                amp_range, sigma_range, nsr_range, seed_type="time", seed=2):
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir, exist_ok=True)
    
    if seed_type == "time":
        np.random.seed(int(time.time()))
    elif seed_type == "fix" and type(seed_type) == int:
        np.random.seed(seed)
    else:
        np.random.seed(2)
    num_list = []
    for i in range(spectrum_num):
        try:
            rnd = np.random.rand(12)
            
            baseline_height = baseline_height_range[0] + rnd[0]*(baseline_height_range[1]-baseline_height_range[0])
            std = std_range[0] + rnd[1]*(std_range[1] - std_range[0])
            sampling_rate = sprate_range[0] + rnd[2]*(sprate_range[1]-sprate_range[0])
            fp = fp_range[0] + rnd[3]*(fp_range[1]-fp_range[0])
            fs = fs_range[0] + rnd[4]*(fs_range[1]-fs_range[0])
            gpass = gpass_range[0] + rnd[5]*(gpass_range[1]-gpass_range[0])
            gstop = gstop_range[0] + rnd[6]*(gstop_range[1]-gstop_range[0])
            peak_num = np.random.randint(peak_num_range[0], peak_num_range[1])
            pos_list = np.random.rand(peak_num)
            pos_list = pos_range[0] + pos_list*(pos_range[1]-pos_range[0])
            amp_list = np.random.rand(peak_num)
            amp_list = amp_range[0] + amp_list*(amp_range[1]-amp_range[0])
            sigma_list = np.random.rand(peak_num)
            sigma_list = sigma_range[0] + sigma_list*(sigma_range[1] - sigma_range[0])
            nsr = nsr_range[0] + rnd[7]*(nsr_range[1]-nsr_range[0])
            
            baseline = add_baseline(width, baseline_height, std)
            baseline = add_butterworth_filter(baseline, sampling_rate, fp, fs, gpass, gstop)
            signal, label, n_peaks = add_peaks(baseline, pos_list, amp_list, sigma_list, label_ci)
            signal = add_noise(baseline, signal, nsr)
            num_list.append(n_peaks)
            np.savez(dataset_dir+f"signal{i}", x=signal, y=label)
            
            del_list = [pos_list, amp_list, sigma_list]
            del rnd, baseline, signal, label, del_list
        except:
            pass
    return np.array(num_list)

def gen_dataset_v2(dict:dict):
    spectrum_num = dict["spectrum_num"]
    width = dict["width"]
    label_ci = dict["label_ci"]
    baseline_height_range = dict["baseline_height_range"]
    std_range = dict["std_range"]
    sprate_range = dict["sprate_range"]
    fp_range = dict["fp_range"]
    fs_range = dict["fs_range"]
    gpass_range = dict["gpass_range"]
    gstop_range = dict["gstop_range"]
    peak_num_range = dict["peak_num_range"]
    pos_range = dict["pos_range"]
    amp_range = dict["amp_range"]
    sigma_range = dict["sigma_range"]
    nsr_range = dict["nsr_range"]
    dataset_id = dict["dataset_id"]
    dataset_dir_root = dict["dataset_dir"]
    dataset_dir = dataset_dir_root+f"/{dataset_id}/"
    height_limit = dict["height_limit"]
    
    try:
        seed_type = dict["seed_type"]
    except:
        seed_type = "time"
    
    if not os.path.exists(dataset_dir):
        os.makedirs(dataset_dir, exist_ok=True)
    
    if dict["reset_dataset"] == True:
        shutil.rmtree(dataset_dir)
        os.makedirs(dataset_dir, exist_ok=True)
    
    if seed_type == "time":
        np.random.seed(int(time.time()))
    elif seed_type == "fix":
        try:
            seed = dict["seed"]
            np.random.seed(seed)
        except:
            np.random.seed(2)
    num_list = []
    for i in tqdm(range(spectrum_num)):
        
        if i >= spectrum_num/2:
            np.random.seed(int(time.time()))
        
        # try:
        rnd = np.random.rand(12)
        
        baseline_height = baseline_height_range[0] + rnd[0]*(baseline_height_range[1]-baseline_height_range[0])
        std = std_range[0] + rnd[1]*(std_range[1] - std_range[0])
        sampling_rate = sprate_range[0] + rnd[2]*(sprate_range[1]-sprate_range[0])
        fp = fp_range[0] + rnd[3]*(fp_range[1]-fp_range[0])
        fs = fs_range[0] + rnd[4]*(fs_range[1]-fs_range[0])
        gpass = gpass_range[0] + rnd[5]*(gpass_range[1]-gpass_range[0])
        gstop = gstop_range[0] + rnd[6]*(gstop_range[1]-gstop_range[0])
        peak_num = np.random.randint(peak_num_range[0], peak_num_range[1])
        pos_list = np.random.rand(peak_num)
        pos_list = pos_range[0] + pos_list*(pos_range[1]-pos_range[0])
        amp_list = np.random.rand(peak_num)
        amp_list = amp_range[0] + amp_list*(amp_range[1]-amp_range[0])
        amp_list_np = np.array(amp_list)
        xx, yy = np.meshgrid(amp_list_np, amp_list_np)
        # try:
        #     distances = np.linalg.norm(amp_list_np[xx]-amp_list_np[yy], axis=2)
        #     distances = np.fill_diagonal(distances, np.nan)
        #     min_distance = np.nanmin(distances)
        # except Exception as e:
        #     print(e)
        sigma_list = np.random.rand(peak_num)
        sigma_list = sigma_range[0] + sigma_list*(sigma_range[1] - sigma_range[0])
        nsr = nsr_range[0] + rnd[7]*(nsr_range[1]-nsr_range[0])
        
        baseline = add_baseline(width, baseline_height, std)
        baseline = add_butterworth_filter(baseline, sampling_rate, fp, fs, gpass, gstop)
        signal, label, n_peaks = add_peaks(baseline, pos_list, amp_list, sigma_list, label_ci)
        signal = add_noise(baseline, signal, nsr)
        
        heigth_current = np.max(signal)
        signal *= height_limit/heigth_current
        
        np.savez(dataset_dir+f"signal{i}", x=signal, y=label)
        num_list.append(n_peaks)
        del_list = [pos_list, amp_list, sigma_list]
        del rnd, baseline, signal, label, del_list
        # except:
        #     pass
    with open(dataset_dir_root+f"/config_{dataset_id}.json", 'w') as f:
        json.dump(dict, f, indent=4)
    return dataset_dir, np.array(num_list)

def visualize_dataset(dataset_dir, num, nrows, ncols, figsize=(10,6), true_peak_nums=None):
    
    filelist = os.listdir(dataset_dir)
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][6:]))[:num]
    print(true_peak_nums)
    l = n = 0
    for i in range(math.ceil(num/(nrows*ncols))):
        filelist_i = filelist[(nrows*ncols)*i:(nrows*ncols)*(i+1)]
        fig, axs = plt.subplots(nrows,ncols, figsize=figsize)
        l = k = 0
        
        for file in filelist_i:
            if num-1 < n:
                break
            data = np.load(dataset_dir+file)
            width = len(data["x"])
            
            if k > 0 and k %ncols == 0:
                l+=1
                k =0
            axs[l,k].plot(range(0, width, 1), data["x"])
            axs[l,k].plot(np.where(data["y"] > 0)[0], data["x"][np.where(data["y"] > 0)], "x")    
            
            try:
                axs[l,k].set_title(true_peak_nums[n])
            except:
                print("dataset doesn't have true label")
            k +=1
            n +=1
        
        plt.show()
        plt.close()
        
def load_data(filepath):
    data = np.load(filepath)
    signal = data["x"]
    label = data["y"]
    return signal, label

if __name__ == "__main__":
    
    file = "../config/dataset.json"
    with open(file) as f:
        settings = json.load(f)
    gen_dataset_v2(settings)