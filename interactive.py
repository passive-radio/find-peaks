import matplotlib.pyplot as plt 
import time
import csv
import numpy as np
import pandas as pd

from findPeaks import findPeaks, read_data, reset_range

x_list = []
y_list = []

X_SCALE = 200
Y_SCALE = 30
count = 0
band = 0
left = 0
right = 0

def draw_test():
    
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
        
        
    plt.plot(x_list, y_list)

    plt.show()

    print(list)
    list = np.array(list)

    path = "pos.csv"

    with open(path, 'w', newline='') as file:
        mywriter = csv.writer(file, delimiter=',')
        mywriter.writerows(list)
        
def plot_test(data, x_list, y_list):
    
    # print(xy_list)
    #xy_list = np.array(xy_list, dtype="float")
    #print(xy_list[0][0], type(xy_list[0][0]))
    
    x_peaks = []
    y_peaks = []
    
    def motion(event):
        is_click_off = False
        global count
        global band
        global left
        global right
        
        if (event.xdata is  None) or (event.ydata is  None):
            return
        
        if event.button == 1 and count == 0:
            count = 1
            x = event.xdata
            y = event.ydata
            
            x_peaks.append(x)
            y_peaks.append(y)
            plt.title(f"Peak selected! at ({int(x)},{int(y)})")
            ax.text(10, 1, "Next, Please select the bandwidth by clicking the edge of the peak! (left->right)")
            
            
        elif event.button == 1 and count == 1:
            left = event.xdata
            count =2
            
        elif event.button == 1 and count == 2:
            right = event.xdata
            band = abs(left- right)
            plt.title(f"Bandwidth selected!: {band}")
            
        plt.draw()
    
    fig = plt.figure()
    ax = fig.add_subplot()
    # plt.figure()
    plt.title("Please click the top of the peak")
    plt.connect('button_press_event', motion)
    plt.scatter(x_list, y_list)
    plt.show()
    
    print("-"*30)
    print("Pointed peak!")
    print("x y bandwidth")
    print(x_peaks[0], y_peaks[0], band)
    print("-"*30)
        
    #data = reset_range(data_origin, 1600)
    findpeaks = findPeaks(data)
    
    #初期値のリストを作成
    #[amp,ctr,wid]
    guess = []
    guess.append([y_peaks[0], x_peaks[0], band])

    #バックグラウンドの初期値
    background = 0

    #初期値リストの結合
    guess_total = []
    for i in guess:
        guess_total.extend(i)
    guess_total.append(background)
    
    popt, pcov = findpeaks.exp_func_fit(*guess_total, mode="g")
    findpeaks.fit_plot(*popt, func="exp")
    
    print("-"*30)
    print("Fitting results!")
    print("x y width")
    print(findpeaks.peakxs[0], findpeaks.peakys[0], findpeaks.peakwidth[0])
    print("-"*30)
        
    plt.show()

if __name__ == "__main__":
    
    base_url = ""
    endpoint = "pos.csv"
    
    x_list = []
    y_list = []
    
    with open(base_url+endpoint, 'r', newline='') as file:
        csv_val = csv.reader(file, delimiter=',')
        for row in csv_val:
            x_list.append(float(row[0]))
            y_list.append(float(row[1]))
    
    data= read_data(base_url + endpoint, 0, ',')
    
    plot_test(data, x_list, y_list)