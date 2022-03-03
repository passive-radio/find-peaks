import csv
from posixpath import split
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def read_data(file, headers, delimineter):
    data = []
    with open(file, "r", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=delimineter)
        for i, row in enumerate(reader):
            if headers < i:
                data.append([float(row[0].replace('\n', '').replace(' ','')), float(row[1].replace('\n', '').replace(' ',''))])
                
    data = pd.DataFrame(data, columns=['x', 'y'])
    return data

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
    xy = np.zeros((len(data.x), int(np.max(data.y)*10**place_num)+1))
    for i in range(len(data.x)):
        dotted_y = int(data.y[i]*10**place_num)
        xy[i][dotted_y] = 1
    return xy