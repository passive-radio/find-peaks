import csv

import matplotlib.pyplot as plt
import numpy as np

from core.preprocessing import read_data, reset_range

def draw_test(file_path, mode):
    
    x_list = []
    y_list = []
    
    X_SCALE = 200
    Y_SCALE = 30
    
    
    def motion(event):
        if (event.xdata is  None) or (event.ydata is  None):
            return
        
        if event.button == 1:
            x = event.xdata
            y = event.ydata
            
            if len(x_list) == 0:
                x_list.append(x)
                y_list.append(y)
            
            if len(x_list) > 0 and (x - x_list[-1])**2 > (X_SCALE/80):
                x_list.append(x)
                y_list.append(y)
            
            ln.set_data(x_list, y_list)
        plt.xlim(0,X_SCALE)
        plt.ylim(0,Y_SCALE)
        plt.draw()
        
    plt.figure()
    ln, = plt.plot([],[],'x')
    plt.connect('motion_notify_event', motion)
    plt.show()

    list = []
    for i in range(len(x_list)):
        list.append([x_list[i], y_list[i]])
        
        
    # plt.plot(x_list, y_list)

    #plt.show()

    print(list)
    list = np.array(list)
    
    try:
        with open(file_path, 'w', newline='') as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(list)
    except FileNotFoundError as e:
        print(f"{e}, please check your file path")
        
    if mode== "rd":
        return read_data(file_path, 0, ",")
    
    if mode=="rp":
        return file_path

