from core.preprocessing import read_data, spectra_image
from utils.labeling import put_labels
from utils.bmp_csv import bmpToCSV
from utils.make_train_data import parsed_data

from tensorflow.keras import optimizers
import matplotlib.pyplot as plt
import numpy as np
import tensorflow as tf
if __name__ == "__main__":
    
    label_file = "../../data/ans_type0.csv"
    x_dir_path = "../../data/atom_linear_spectrum/"
    x_data, y_data = parsed_data(label_file, x_dir_path)
    