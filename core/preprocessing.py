from calendar import day_abbr
import csv
from email import header
from email.headerregistry import HeaderRegistry
from operator import contains
import os
from tkinter.tix import Tree
from wsgiref import headers
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2

from numpy import arange

from numpy import column_stack

def res_img_filee(dir_path, width, height):
    filelist = os.listdir(dir_path)
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][15:]))
    filelist = filelist[:100]
    
    np_images = []
    for file in filelist:
        img = read_data(dir_path + file, headers=-1, delimineter=",")
        img = spectra_image(img)
        ratio_y = height/img.shape[0]
        ratio_x = width/img.shape[1]
        img = cv2.resize(img, dsize=None, fx=ratio_x, fy=ratio_y,interpolation=cv2.INTER_LANCZOS4)
        np_images.append(img)
        
    np_images = np.array(np_images)
    return np_images

def read_data(file, delimiter=None, headers=None, footers=None, errors="ignore", contains_x_axis=True):
    data = []
    with open(file, "r", encoding="utf-8", errors=errors) as f:
        reader =csv.reader(f, delimiter=delimiter)
        for i, row in enumerate(reader):
            if row == "":
                break
            elif headers < i < footers:
                data.append([col.replace('\n', '').replace(' ','') for col in row])
    data = pd.DataFrame(data)
    if len(data.columns) == 1 and not contains_x_axis:
        data = data.reset_index()
        data = data.set_axis(["x", "y"], axis="ignore")
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
        print("Warning: contains_x_axis is True but the number of the columns is 1. X value might be converted as y.")
    return data

def get_raw_x_data(x_dir_path, delimineter, headers=None, footers=None):
    filelist = os.listdir(x_dir_path)
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][15:]))
    
    np_images = []
    for file in filelist:
        data = read_data(x_dir_path+file, delimineter=delimineter, headers=headers, footers=footers)
        data = spectra_image(data)
        del data
        np_images.append(data)
    np_images = np.array(np_images)
    return np_images



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
        
def spectra_image(data):
    # xy = np.zeros((len(data.x),len(data.y)))
    y_ini = str(data.y[0])
    y_s, y_d = y_ini.split('.')
    place_num = len(y_d)
    place_num = 3
    height = int(np.max(data.y)*10**(place_num-3)+1)
    xy = np.zeros((height, len(data.x)))
    for i in range(len(data.x)):
        dotted_y = int(data.y[i]*10**(place_num-3))
        xy[height-dotted_y:height,i] = 1
        del dotted_y
    return xy


def resize_dir_image(dir_path, width, height):
    filelist = os.listdir(dir_path)
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][15:]))
    # filelist = filelist[:100]
    
    np_images = []
    for file in filelist:
        img = read_data(dir_path + file, headers=-1, delimineter=",")
        img = spectra_image(img)
        ratio_y = height/img.shape[0]
        ratio_x = width/img.shape[1]
        img = cv2.resize(img, dsize=None, fx=ratio_x, fy=ratio_y,interpolation=cv2.INTER_LANCZOS4)
        np_images.append(img)
        
    np_images = np.array(np_images)
    return np_images

def resized_x_data(x_data, width=None, height=None, ratio_x=None, ratio_y=None):
    
    np_images = []
    for img in x_data:
        if ratio_x == None:
            try:
                ratio_x = height/img.shape[0]
                ratio_y = width/img.shape[1]
                img = cv2.resize(img, dsize=None, fx=ratio_x, fy=ratio_y, interpolation=cv2.INTER_LANCZOS4)
                np_images.append(img)
            except Exception as e:
                print(e)
                return
                
        elif width == None:
            try:
                img == cv2.resize(img, dsize=None, fx=ratio_x, fy=ratio_y, interpolation=cv2.INTER_LANCZOS4)
                np_images.append(img)
            except Exception as e:
                print(e)
                return
    np_images = np.array(np_images)
    return np_images


if __name__ == "__main__":
    file = "../../data/proportional_tubes_x_ray/spectrum_type2_0.mca"    
    file = "../../data/atom_linear_spectrum/spectrum_type0_0.csv"
    data = read_data(file, ",", headers=11, footers=1036, errors="ignore", contains_x_axis=True)
    print(data.head(3))