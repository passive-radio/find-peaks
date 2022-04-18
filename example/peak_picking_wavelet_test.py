from random import gauss
import sys
sys.path.append("../")
sys.path.append("core/")

import numpy as np
import pandas as pd
from core import wavelet_detection
from utils import gen_spectra

def main():
    filepath = "sample_data/sim01.csv"
    signal = gen_spectra.gen_sim_signal(width=2000, baseline_height=20, baseline_std=20, peak_pos=300,
                                peak_scale=50, gauss_a=30, gauss_mu=0, gauss_sigma=50, noise_scale=1)
    df = pd.DataFrame(signal)
    df.to_csv(filepath,sep=",")
    wavelet_detection.to_scalogram(filepath, width=1, wavelet_span=2, Fs=10, soft_max_c=1e-6)
    
    # base_path = "../data/atom_linear_spectrum/"
    # wavelet_detection.to_scalogram_dir(base_path, ",", 0, 640, width=0.1, wavelet_span=10, Fs=20, soft_max_c=1e-12)
    
main()