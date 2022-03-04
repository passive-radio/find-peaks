from distutils import filelist
from fileinput import filelineno
from importlib.machinery import PathFinder
from lib2to3.pytree import BasePattern
import os
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from keras.layers import Activation, Conv2D, Dense, Flatten, MaxPool2D, Dropout
from keras.models import Sequential, load_model
from keras.utils.np_utils import to_categorical
from keras.utils.vis_utils import plot_model
import keras
from keras.datasets import mnist

from core.preprocessing import read_data, spectra_image
from utils.labeling import put_labels
from utils.bmp_csv import bmpToCSV
from utils.make_train_data import parsed_data

if __name__ == "__main__":
    
    label_file = "../../data/ans_type0.csv"
    x_dir_path = "../../data/atom_linear_spectrum/"
    x_data, y_data = parsed_data(label_file, x_dir_path)
    