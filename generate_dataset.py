import json
from utils.dataset import gen_dataset, gen_dataset_v2

def main():
    file = "config/dataset.json"
    with open(file) as f:
        settings = json.load(f)
    
    dataset_dir = f"../data/dataset/"
    
    # gen_dataset(settings["spectrum_num"], settings["width"], 
    #             dataset_dir, settings["label_ci"], settings["baseline_height_range"],
    #             settings["std_range"], settings["sprate_range"],settings["fp_range"],
    #             settings["fs_range"], settings["gpass_range"], settings["gstop_range"],
    #             settings["peak_num_range"], settings["pos_range"], settings["amp_range"],
    #             settings["sigma_range"], settings["nsr_range"])
    gen_dataset_v2(settings)
main()

