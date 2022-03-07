from codecs import ignore_errors
import csv
from dataclasses import dataclass
from email import header
import os
from turtle import end_fill
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import cv2

from numpy import arange

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

def read_data(file, delimineter, headers=None, footers=None):
    data = []
    with open(file, "r", encoding="utf-8") as f:
        data = f.readline()
        print(data)
        reader = csv.reader(f, delimiter=delimineter)
        if headers == None and footers==None:
            range_data = np.array(len(reader)).astype(np.int32)
        elif headers != None and footers == None:
            range_data = np.arange(start=headers+1, stop=len(reader)-1, step=1).astype(np.int32)
        elif headers == None and footers != None:
            range_data = np.arange(start=0, stop=footers-1, step=1).astype(np.int32)
        elif headers != None and footers != None:
            range_data = np.arange(start=headers+1, stop=footers-1, step=1).astype(np.int32)
        df = pd.read_csv(file, sep=",", on_bad_lines="skip")
        df.reset_index()
        df.set_axis(["x", "y"], axis="columns")
        print(df.head(5))
        for i in range_data:
            try:
                if headers < i:
                # print(str in row)
                    data.append([float(reader[i][0].replace('\n', '').replace(' ','')), float(reader[i][1].replace('\n', '').replace(' ',''))])
            except IndexError as e:
                """"""
    del reader
    data = pd.DataFrame(data, columns=['x', 'y'])
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