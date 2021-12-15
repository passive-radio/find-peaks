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
peak_count = 0
texts = []



def draw_test(file_path, mode):
    
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
        print(f"{e}, please verify your file path")
        
    if mode== "wrd":
        return read_data(file_path, 0, ",")
    
    if mode=="wrp":
        return file_path

        
            
def plot_test(data):
    
    x_list = data.x
    y_list = data.y
    
    # print(xy_list)
    #xy_list = np.array(xy_list, dtype="float")
    #print(xy_list[0][0], type(xy_list[0][0]))
    
    x_peaks = []
    y_peaks = []
    bands = []
    
    def button_pressed_motion(event):
        is_click_off = False
        global count
        global band
        global left
        global right
        global texts
        global peak_count
        
        #[event] event.button
        # value | info
        #   1   |   left-click
        #   2   |   mouse wheeling
        #   3   |   right-click
        
        if (event.xdata is  None) or (event.ydata is  None):
            return
        
        if event.button == 1 and count == 0:
            count = 1
            x = event.xdata
            y = event.ydata
            
            x_peaks.append(x)
            y_peaks.append(y)
            plt.title(f"Peak selected! at ({int(x)},{int(y)})")
            #texts.append(ax.text(100, 30, "Next, Please select the bandwidth by clicking the edge of the peak! (left->right)"))
            
        elif event.button == 1 and count == 1:
            left = event.xdata
            count =2
            
        elif event.button == 1 and count == 2:
            right = event.xdata
            band = abs(left- right)
            bands.append(band)
            #texts[peak_count].remove()
            plt.title(f"Bandwidth selected!: {band}")
            ax.text(100, 30, "You can now close this window!")
        
        if event.button == 3 and count == 2:
            plt.title(f"Now, select next peak!")
            peak_count += 1
            count = 0
            
        plt.draw()
    
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.title("Please click the top of the peak! :)")
    plt.connect('button_press_event', button_pressed_motion)
    plt.scatter(x_list, y_list, s=2)
    plt.show()
    
    
        
    #data = reset_range(data_origin, 1600)
    findpeaks = findPeaks(data)
    
    #初期値のリストを作成
    #[amp,ctr,wid]
    guess = []
    for i in range(len(x_peaks)):
        try:
            guess.append([x_peaks[i], y_peaks[i], bands[i]])
        except Exception as e:
            print(e)
            pass

    #バックグラウンドの初期値
    background = 0

    #初期値リストの結合
    guess_total = []
    for i in guess:
        guess_total.extend(i)
    guess_total.append(background)
    
    popt, pcov = findpeaks.exp_func_fit(*guess_total, mode="g")
    findpeaks.fit_plot(*popt, func="exp")
    
    
    for i in range(len(x_peaks)):
        
        print("Fitting results")
        print("-"*30)
        print(f"Pointed peak {i}")
        print("x y bandwidth")
        print(x_peaks[i], y_peaks[i], bands[i])
        print("Fitting results")
        print("x y width")
        print(findpeaks.peakxs[i], findpeaks.peakys[i], findpeaks.peakwidth[i])
        print("-"*30)
    

    plt.show()
    
def seeSpectrum(data):
    
    x_list = data.x
    y_list = data.y
    
    plt.title("")
    plt.scatter(x_list, y_list, s=2)
    plt.show()
    
if __name__ == "__main__":
    
    base_url = "sample_data/"
    endpoint = "sample02.csv"
    
    # x_list = []
    # y_list = []
    # with open(base_url+endpoint, 'r', newline='') as file:
    #     csv_val = csv.reader(file, delimiter=',')
    #     for row in csv_val:
    #         x_list.append(float(row[0]))
    #         y_list.append(float(row[1]))
    
    data= read_data(base_url + endpoint, 0, ',')
    
        
    plot_test(data)
