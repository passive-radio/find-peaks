import os

import pandas as pd
import numpy as np
from numpy import arange
from tqdm import tqdm
import matplotlib.pyplot as plt

import sys
sys.path.append('../')

from core.preprocessing import read_data, spectra_image, reset_range
from utils.labeling import put_labels

def x_data_dir_all(dir_path):
    filelist = os.listdir(dir_path)[:100]
    max_height = 1
    np_image_list = []
    
    for i,file in enumerate(filelist):
        data = read_data(dir_path + file, headers=-1, delimineter=",")
        np_image = spectra_image(data)
        
        if np_image.shape[0] > max_height:
            max_height = np_image.shape[0]
        np_image_list.append(np_image)
        del data, np_image
    # np_images = np.array([np_image_list[i] for i in range(len(np_image_list))])
    return np_image_list, max_height

def label_dir_all(dir_path, path_save, way):
    filelist = os.listdir(dir_path)[:100]
    y_labels = []
    
    for file in filelist:
        data = read_data(dir_path + file, headers=-1, delimineter=",")
        labeller = put_labels(data=data, mode=way)
        
        if way == "click":
            x_peaks, _ = labeller.put_labels()
            print(x_peaks)
            y_labels.append(x_peaks)
            
        if way == "drag":
            x12_peaks, y12_peaks = labeller.put_labels()
            y_labels.append(x12_peaks)
            # y_labels.append(arange(start=x1_peaks, stop=x2_peaks, step=1))
            
    if way == "drag":
        return y_labels
    
    df = pd.DataFrame(y_labels)
    print(df)
    del y_labels
    # df.to_csv(path_save, sep=",")
    return df

def y_data_all(df, y_width, label_file_base):
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
            
    df_ans = pd.DataFrame(label)
    df_ans.to_pickle(label_file_base + ".pkl")
    df_ans.to_csv(label_file_base+".csv")
    del df_ans
    return label

def y_data_all_drag(y_labels, y_width, label_file_base):
    
    label = np.zeros(shape=(len(y_labels), y_width))
    for i, y_label in enumerate(y_labels):
        for y_band in y_label:
            if type(y_band[0]) == np.float64:
                if y_band[0] < y_band[1]:
                    y_left_edge = int(y_band[0])
                    y_right_edge = int(y_band[1])
                else:
                    y_left_edge = int(y_band[1])
                    y_right_edge = int(y_band[0])
                if y_left_edge < 0:
                    y_left_edge = 0
                if y_right_edge > y_width:
                    y_right_edge = y_width
                    
                label[i][y_left_edge: y_right_edge] = 1
                print(y_left_edge, y_right_edge)
                
    df_ans = pd.DataFrame(label)
    df_ans.to_pickle(label_file_base+".pkl")
    df_ans.to_csv(label_file_base+".csv")
    del df_ans
    return label

def parsed_data(label_path_base, x_dir_path, way, new_data=True):
    np_images, max_height = x_data_dir_all(x_dir_path)
    x_data = make_same_size_np_image(np_images, max_height)
    y_width = np_images[0].shape[1]
    
    if way == "click":
        df = label_dir_all(x_dir_path, label_path_base, way)
        # df = pd.read_csv(label_file)
        y_data = y_data_all(df, y_width, label_path_base)
        
    elif way == "drag" and new_data==True:
        y_labels = label_dir_all(x_dir_path, label_path_base, way)
        y_data = y_data_all_drag(y_labels, y_width, label_path_base)
    
    elif way == "drag" and new_data == False:
        try:
            y_data = pd.read_pickle(label_path_base+".pkl")
        except:
            y_data = pd.read_csv(label_path_base+".csv")
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
    
    label_path_base = '../../data/ans_type0'
    x_dir_path = '../../data/atom_linear_spectrum/'
    x_data, y_data = parsed_data(label_path_base, x_dir_path, way="drag", new_data=False)
    print(x_data.shape, y_data.shape)
    
    # print(x_data[0].shape)
    # print(np.where(y_data > 0.5))
    
    # plt.imshow(x_data[2])
    # plt.show()