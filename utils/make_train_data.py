from cmath import atanh
from distutils import filelist
import os
from re import X
from shutil import ignore_patterns
from turtle import RawTurtle
from urllib.parse import MAX_CACHE_SIZE
from matplotlib.pyplot import ylabel

import pandas as pd
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

import sys
sys.path.append('../')

from core.preprocessing import read_data, spectra_image, reset_range
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
    return df
    df.to_csv(path_save, sep=",")
    del df
    
def x_data_dir_all(dir_path):
    filelist = os.listdir(dir_path)[:100]
    max_height = 1
    np_image_list = []
    
    for i,file in enumerate(filelist):
        data = read_data(dir_path + file, headers=-1, delimineter=",")
        np_image = spectra_image(data)
        
        if np_image.shape[0] > max_height:
            max_height = np_image.shape[0]
            print(max_height)
        np_image_list.append(np_image)
        del data, np_image
    # np_images = np.array([np_image_list[i] for i in range(len(np_image_list))])
    return np_image_list, max_height

def y_data_all(df, y_width):
    y_labels = df
    y_labels.set_axis(["x", "y1", "y2"], axis="columns", inplace=True)
    
    label = np.zeros(shape=(len(y_labels), y_width))
    for y_label in y_labels.itertuples():
        index = y_label.x
        if y_label.y1 is not np.nan and not y_label.y1 != y_label.y1:
            y1 = int(y_label.y1)
            if y1 > y_width:
                y1 = int(y_width -1)
            # print(y1)
            label[index][y1] = 1
        
        if y_label.y2 is not np.nan and not y_label.y2 != y_label.y2:
            y2 = int(y_label.y2)
            if y2 > y_width:
                y2 = int(y_width -1)
            label[index][y2] = 1
            # print(y2)
    return label

def parsed_data(label_file, x_dir_path):
    
    np_images, max_height = x_data_dir_all(x_dir_path)
    x_data = make_same_size_np_image(np_images, max_height)
    
    # df = label_dir_all(x_dir_path, label_file)
    df = pd.read_csv(label_file)
    y_width = np_images[0].shape[0]
    y_data = y_data_all(df, y_width)
    
    return x_data, y_data

def make_same_size_np_image(x_data, max_height):
    
    np_images = []
    for x in tqdm(x_data):
        shape = x.shape
        zeros = np.zeros(shape=(max_height, shape[1]))
        zeros[max_height-shape[0]:max_height, 0:shape[1]] = x
        np_images.append(zeros)
    
    np_images = np.array(np_images)
    return np_images

if __name__ == "__main__":
    
    label_file = "../../data/ans_type0.csv"
    x_dir_path = "../../data/atom_linear_spectrum/"
    x_data, y_data = parsed_data(label_file, x_dir_path)
    # print(x_data.shape, y_data.shape)
    
    # print(x_data[0].shape)
    
    # print(np.where(y_data > 0.5))
    
    plt.imshow(x_data[2])
    plt.show()