from cmath import atanh
from distutils import filelist
import os
from shutil import ignore_patterns

import pandas as pd
import numpy as np

from core.preprocessing import read_data, spectra_image
from utils.labeling import put_labels

def label_dir_all(dir_path, path_save):
    filelist = os.listdir(dir_path)
    y_labels = []
    
    for file in filelist:
        data = read_data(dir_path + file, headers=-1, delimineter=",")
        labeller = put_labels(data=data, mode="click")
        x_peaks, _ = labeller.put_labels()
        print(x_peaks)
        y_labels.append(x_peaks)
    
    df = pd.DataFrame(y_labels)
    del y_labels
    df.to_csv(path_save, sep=",")
    del df

def parsed_data(label_file, x_dir_path):
    
    file = "sample_data/sample04.csv"
    data = read_data(file, headers=-1, delimineter=",")
    
    np_image = spectra_image(data)
    
    y_labels = pd.read_csv(file, sep=",")
    y_labels.set_axis(["x", "y1", "y2"], axis="columns", inplace=True)
    sample_data = read_data("../data/atom_linear_spectrum/spectrum_type0_0.csv", headers=-1, delimineter=",")
    y_width = len(sample_data)


    for y_label in y_labels.itertuples():
        index = y_label.x
        label = np.zeros(shape=(len(y_labels), y_width))
        if y_label.y1 is not np.nan and not y_label.y1 != y_label.y1:
            y1 = int(y_label.y1)
            
            if y1 > y_width:
                y1 = int(y_width -1)
            label[index][y1] = 1

    print(label, label.shape)