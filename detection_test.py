import sys
sys.path.append("../")
sys.path.append("core/")

import numpy as np
import pandas as pd
from core import wavelet_detection
from utils import gen_spectra

def main():
    filepath = "sample_data/sim01.csv"
    signal = gen_spectra.gen_sim_signal(2000, 10, 10, 200, 50, 100, 0, 10, 2)
    
    df = pd.DataFrame(signal)
    df.to_csv(filepath,sep=",")
    
    wavelet_detection.to_scalogram(filepath, width=1, wavelet_span=2, Fs=10, soft_max_c=1e-6)
    
main()