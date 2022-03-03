from distutils import filelist
from fileinput import filelineno
from importlib.machinery import PathFinder
from lib2to3.pytree import BasePattern
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
# from keras.layers import Activation, Conv2D, Dense, Flatten, MaxPool2D, Dropout
# from keras.models import Sequential, load_model
# from keras.utils.np_utils import to_categorical
# from keras.utils.vis_utils import plot_model
# import keras
# from keras.datasets import mnist

from core.preprocessing import read_data, spectra_image
from utils.labeling import put_labels
from utils.bmp_csv import bmpToCSV

if __name__ == "__main__":
    file = "sample_data/sample04.csv"
    data = read_data(file, headers=-1, delimineter=",")
    
    np_image = spectra_image(data)
    print(np_image.shape)
    
    base_path = "../data/atom_linear_spectrum/"
    # y_labels = []
    # file_list = os.listdir(base_path)[:100]
    # for file in file_list:
    #     data = read_data(base_path + file, headers=-1, delimineter=",")
    #     labeller = put_labels(data=data, mode="click")
    #     x_peaks, _ = labeller.put_labels()
    #     print(x_peaks)
    #     y_labels.append(x_peaks)
    
    # df = pd.DataFrame(y_labels)
    # df.to_csv("../data/ans_type0.csv", sep=",")
    
    y_labels = pd.read_csv("../data/ans_type0.csv", sep=",")
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
    # labeller = put_labels(data=data, mode="click")
    # x_peaks, y_peaks = labeller.put_labels()
    # print(x_peaks)
    # (X_train, y_train), (X_test, y_test) = mnist.load_data()
    # print(X_train[0], X_train.shape)
    # print(y_train[0], y_train.shape)
    
    