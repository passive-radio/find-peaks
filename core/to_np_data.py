from nntplib import NNTPPermanentError
from operator import contains
import os
from tkinter.tix import Tree
from turtle import width
from wsgiref import headers
import pandas as pd
import numpy as np
from tensorboard import errors
from numpy import reshape
from tqdm import tqdm
import matplotlib.pyplot as plt
import sys
import cv2
import csv

sys.path.append('utils/')
sys.path.append('../')

from labeling import put_labels

def read_file(file, delimiter=None, headers=None, footers=None, errors="ignore", contains_x_axis=True):
    data = []
    if headers == None:
        headers = -1
    with open(file, "r", encoding="utf-8", errors=errors) as f:
        reader =csv.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if footers != None and i >= footers:
                break
            if row == "" or row == None:
                continue
            elif headers < i :
                data.append([col.replace('\n', '').replace(' ','') for col in row])
    data = pd.DataFrame(data)
    if len(data.columns) == 1 and not contains_x_axis:
        data = data.reset_index()
        data = data.set_axis(["x", "y"], axis="columns")
    elif len(data.columns) == 2 and contains_x_axis:
        data = data.set_axis(["x", "y"], axis="columns")
    elif len(data.columns) > 2 and contains_x_axis:
        data = data.set_axis([f"y{i-1}" for i in range(len(data.columns))], axis="columns")
        data = data.rename(columns={"y-1": "x"})
    elif len(data.columns) > 1 and not contains_x_axis:
        data = data.reset_index()
        data = data.set_axis([f"y{i-1}" for i in range(len(data.columns))], axis="columns")
        data = data.rename(columns={"y-1": "x"})
    elif len(data.columns) == 1 and contains_x_axis:
        data = data.reset_index()
        data = data.set_axis(["x", "y"], axis="columns")
        # print("Warning: contains_x_axis is True but the number of the columns is 1. X value might be converted as y.")
    return data

def to_x_data(x_dir_path, delimiter, method:str, to_x_data_method:str, height=None, width=None, headers=None, footers=None, errors="ignore", contains_x_axis=True):
    filelist = os.listdir(x_dir_path)
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][15:]))
    
    np_images = []
    for file in tqdm(filelist):
        data = read_file(x_dir_path+file, delimiter=delimiter, headers=headers, footers=footers, errors=errors, contains_x_axis=contains_x_axis)
        data = spectra_to_np_array(data, to_x_data_method=to_x_data_method)
        np_images.append(data)
    x_data = to_same_shape(np_images, method, height=height, width=width)
    del np_images
    return x_data

def to_same_shape(x_data_list, resize_method:str, height=None, width=None) -> np.array:
    if resize_method == "expand":
        x_data = to_same_shape_by_expand(x_data_list, height, width)
        
    elif resize_method == "fill":
        x_data = to_same_shape_by_fill(x_data_list)
    return x_data

def to_same_shape_by_expand(x_data_list, height, width, ratio_x=None, ratio_y=None):
    np_images = []
    for x in x_data_list:
        if ratio_x == None:
            try:
                img = cv2.resize(x, dsize=None, fx=width/x.shape[1], fy=height/x.shape[0],
                                interpolation=cv2.INTER_LANCZOS4)
                np_images.append(img)
            except Exception as e:
                print(e)
                return
                
        elif width == None:
            try:
                img == cv2.resize(x, dsize=None, fx=ratio_x, fy=ratio_y, interpolation=cv2.INTER_LANCZOS4)
                np_images.append(x)
            except Exception as e:
                print(e)
                return
    np_images = np.array(np_images)
    x_data = np_images
    del np_images
    return x_data

def to_same_shape_by_fill(x_data_list):
    max_height = 0
    for np_image in x_data_list:
        if np_image.shape[0] > max_height:
            max_height = np_image.shape[0]
            
    np_images = []
    for x in x_data_list:
        shape = x.shape
        zeros = np.zeros(shape=(max_height, shape[1]))
        zeros[max_height-shape[0]:max_height, 0:shape[1]] = x
        np_images.append(zeros)
    
    np_images = np.array(np_images)
    x_data = np_images
    del np_images
    return x_data

def reset_range(data, start=None, end=None):
    try:
        if type(start) == int and type(end)==int:
            return data[start:end]
        elif start == None and type(end)==int:
            return data[0,end]
        elif type(start)==int and end==None:
            return data[start:]
        else:return data
    except Exception as e:
        print("Error: xrange should be specified!(=> [x_start, x_end])")
        
def spectra_to_np_array(data, to_x_data_method="fill"):
    
    if to_x_data_method == "fill":
        x_data = to_x_data_by_fill(data)
    elif to_x_data_method == "dot":
        x_data = to_x_data_by_dot(data)
    return x_data

def to_x_data_by_fill(data):
    y_ini = str(data.y[0])
    splited_num = y_ini.split('.')
    if len(splited_num) == 1:           # ->natural number
        height_multiple = 1
    else:
        _, y_d = y_ini.split('.')
        # print(len(y_d))
        height_multiple = 10**int(len(y_d)/3)
    
    data.x = np.array(data.x).astype(np.int32)
    data.y = np.array(data.y).astype(np.float32)
    height = np.max(data.y)
    width = len(data.x)
    
    xy = np.zeros((int(height*height_multiple + 1), width*height_multiple))
    for i in range(len(data.x)):
        dotted_y = int(data.y[i]*height_multiple)
        if height_multiple > 1:
            xy[int(height*height_multiple)-dotted_y:int(height*height_multiple),i*height_multiple:(i+1)*height_multiple-1] = 1
        else:
            xy[int(height*height_multiple)-dotted_y:int(height*height_multiple),i] = 1
        del dotted_y
    return xy

def to_x_data_by_dot(data):
    data.y = np.array(data.y).astype(np.float32)
    return data.y.values

class anotating_data(object):
    def __init__(self, x_data) -> None:
        self.x_data = x_data
        self.width = x_data.shape[2]
        del x_data
        
    def get_y_data(self, method):
        self.method = method
        y_data_df = self.get_y_df()
        
        if method == "click":
            y_data = self.data_from_clicked(y_data_df)
            
        elif method == "drag":
            y_data = self.data_from_draged(y_data_df)
        self.y_data = y_data
        del y_data
        return self.y_data
    
    def get_y_df(self):
        x_data = self.x_data[:3]
        y_labels = []
        for data in x_data:
            labeller = put_labels(data, mode=self.method)
            x_peaks, _ = labeller.put_labels()
            y_labels.append(x_peaks)
        y_data = pd.DataFrame(y_labels)
        return y_data
        
    def data_from_draged(self, y_data_df):
        width = self.width
        
        label = np.zeros(shape=(len(y_data_df), width))
        for i, y_label in y_data_df.iterrows():
            for y_band in y_label:
                print(y_band)
                if y_band == None:
                    continue
                if type(y_band[0]) == np.float64:
                    if y_band[0] < y_band[1]:
                        y_left_edge = int(y_band[0])
                        y_right_edge = int(y_band[1])
                    else:
                        y_left_edge = int(y_band[1])
                        y_right_edge = int(y_band[0])
                    if y_left_edge < 0:
                        y_left_edge = 0
                    if y_right_edge > width:
                        y_right_edge = width
                        
                    label[i][y_left_edge: y_right_edge] = 1
        y_data = label
        del label, y_data_df
        return y_data
    
    def data_from_clicked(self, y_data_df):
        y_labels = y_data_df
        del y_data_df
        width = self.width
        y_labels.set_axis(["x", "y1", "y2"], axis="columns", inplace=True)
        
        label = np.zeros(shape=(len(y_labels), width))
        for y_label in y_labels.itertuples():
            index = y_label.x
            if y_label.y1 is not np.nan and not y_label.y1 != y_label.y1:
                y1 = int(y_label.y1)
                if y1 > width:
                    y1 = int(width -1)
                # print(y1)
                label[index][y1] = 1
            
            if y_label.y2 is not np.nan and not y_label.y2 != y_label.y2:
                y2 = int(y_label.y2)
                if y2 > width:
                    y2 = int(width -1)
                label[index][y2] = 1
        y_data = label
        del label
        return y_data
    
    def read_y_data(self, save_path, sep :str) -> np.array:
        dir = os.path.dirname(save_path)
        filebase = os.path.basename(save_path).split('.', 1)[0]
        try:
            y_data = pd.read_pickle(dir+filebase+".pkl")
            y_data = y_data.values
            
        except:
            y_data = pd.read_csv(dir+filebase+".csv", sep=sep)
            y_data = y_data.values
            y_data = np.delete(y_data, 0, axis=1)
        return y_data

def to_xy_data(x_dir_path:str, delimiter:str, label_way:str, to_x_data_method:str, reshape_method:str,
                width=None, height=None, headers=None, footers=None,
                ratio_x=None, ratio_y=None, errors="ignore", contains_x_axis=True):
    x_data = to_x_data(x_dir_path, delimiter, to_x_data_method=to_x_data_method, method=reshape_method, width=width, height=height, headers=headers,
                        footers=footers, errors=errors, contains_x_axis=contains_x_axis)
    # print(x_data.shape)
    anotating = anotating_data(x_data)
    y_data = anotating.get_y_data(method=label_way)
    # y_data = pd_to_np_y("../../data/ans_type1.csv")

    return x_data, y_data

def pd_to_np_y(label_filepath, y_filepath=None):
    y_data = pd.read_csv(label_filepath)
    y_data = y_data.values
    y_data = np.delete(y_data, 0, axis=1)
    # np.save(y_filepath, y_data)
    return y_data

def read_xy_data(x_filepath, y_filepath):
    x_data = np.load(x_filepath)
    y_data = np.load(y_filepath)
    return x_data, y_data

def save_data(x_data, y_data, x_filepath:str, y_filepath:str, type="csv"):
    dir = os.path.dirname(x_filepath)+"/"
    filebase = os.path.basename(x_filepath).split('.', 1)[0]
    try:
        np.save(dir+filebase, x_data)
    except:
        print("Fail to save x_data")
    dir = os.path.dirname(y_filepath)+"/"
    filebase = os.path.basename(y_filepath).split('.', 1)[0]
    try:
        np.save(dir+filebase, y_data)
    except:
        print("Fail to save y_data")
    # print("x_data, y_data are saved!")

if __name__ == "__main__":
    
    x_dir_path = '../../data/gamma_ray/'
    x_data, y_data = to_xy_data(x_dir_path, ",", to_x_data_method="fill", label_way= "drag", 
                                reshape_method= "expand",width=640, height=640, 
                                headers=-1, footers=640, contains_x_axis=True)
    print(x_data.shape, y_data.shape)
    
    # x_filepath = '../../data/ans_type1_x.npy'
    # y_filepath = '../../data/ans_type1_y.npy'
    # save_data(x_data, y_data, x_filepath=x_filepath, y_filepath=y_filepath, type="npy")
    