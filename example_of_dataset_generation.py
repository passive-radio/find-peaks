"""
It is highly recommended to use any simulated dataset generator class defined in Signal instead of gen_dataset_old or gen_dataset_v2_old.
"""

import json
import sys
import time

sys.path.append("../")
sys.path.append("Signal/")
sys.path.append("Module/")

from Signal.generator import sequence_generator
from utils.dataset import visualize_dataset, gen_dataset_v2_old

def main():
    
    file = "config/dataset.json"
    with open(file) as f:
        settings = json.load(f)
    log_config_path = "config/log_config.json"
    
    start = time.time()
    dataset_dir, n_peaks = gen_dataset_v2_old(settings, log_config_path)
    print(f"elapsed time: {time.time() - start}")
    
    visualize_dataset(dataset_dir, 2, 5, num=10, true_peak_nums=n_peaks)
    
    return None

def main_v2():
    file = "config/dataset.json"
    with open(file) as f:
        settings = json.load(f)
    log_config_path = "config/log_config.json"
    
    start = time.time()
    dataset_dir, n_peaks = sequence_generator(settings, log_config_path)
    print(f"elapsed time: {time.time() - start}")
    
    visualize_dataset(dataset_dir, 2, 5, num=10, true_peak_nums=n_peaks)
    
    return None


if __name__ == "__main__":
    """
    It is highly recommended to use any simulated dataset generator class defined in Signal instead of gen_dataset_old or gen_dataset_v2_old.
    """
    
    main_v2()
    main()