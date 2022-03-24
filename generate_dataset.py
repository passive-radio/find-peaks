import json
import sys
import numpy as np

sys.path.append("core/")
sys.path.append('utils/')
sys.path.append('../')

import utils.dataset as dataset
import numpy
from utils.dataset import gen_dataset_v2, visualize_dataset, load_data
from core.wavelet_detection import to_scalogram, to_scalogram_dir

def main():
    file = "config/dataset.json"
    with open(file) as f:
        settings = json.load(f)
    
    dataset_dir = f"../data/atom_linear_spectrum/"
    # dataset_dir_path, n_peaks_list = gen_dataset_v2(settings)
    # visualize_dataset(dataset_dir_path, 100, 2, 5, figsize=(13,6), true_peak_nums=n_peaks_list)
    to_scalogram_dir(dataset_dir, width=1, wavelet_span=2, Fs=10, soft_max_c=1e-10, num_sort_pos=15)
    # for i in range(20):
    #     filepath = dataset_dir+f"signal{i}.npz"
    #     to_scalogram(filepath, width=1, wavelet_span=2, Fs=10, soft_max_c=1e-10)

main()

