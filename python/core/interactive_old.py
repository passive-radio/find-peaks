import matplotlib.pyplot as plt 
import matplotlib.patches as patches
from matplotlib.artist import Artist
import csv
import numpy as np
import pandas as pd

from core.detection import find_peaks
from core.preprocessing import read_data

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
DragFlag = False
draw_count = 0
rs = []
is_released = False

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
    DragFlag = False    
    
    def button_pressed_motion(event):
        is_click_off = False
        global count
        global band
        global left
        global right
        global texts
        global peak_count
        global x1, y1
        global DragFlag
        global is_released
        global sx1, sx2, sy1, sy2
        
        #[event] event.button
        # value | info
        #   1   |   left-click
        #   2   |   mouse wheeling
        #   3   |   right-click
        
        if (event.xdata is  None) or (event.ydata is  None):
            return
        
        # if event.button == 1 and not DragFlag:
        #     count = 1
        #     x1 = event.xdata
        #     y1 = event.ydata
            
        #     DragFlag = True
        plt.title("mouse clicked!")
        
        if DragFlag == False:        
            x1 = event.xdata
            y1 = event.ydata
            DragFlag = True
            
            # x_peaks.append(x)
            # y_peaks.append(y)
            # plt.title(f"Peak selected! at ({int(x)},{int(y)})")
            #texts.append(ax.text(100, 30, "Next, Please select the bandwidth by clicking the edge of the peak! (left->right)"))
            
        if event.button == 3 and count == 1:
            plt.title(f"Now, select next peak!")
            peak_count += 1
            count = 0
            
        if is_released == True:
            plt.title("right click to verify if this select is fine or select peak again!")
            
        if event.button == 3:
            iy1,iy2 = sorted([sy1,sy2])
            x_peaks.append((sx1+sx2)/2)
            y_peaks.append(iy2)
            bands.append(abs(sx1-sx2))
            
        plt.draw()
        
    # 四角形を描く関数
    def DrawRect(x1,x2,y1,y2):
        global rs,rold, draw_count
        global sx1, sx2, sy1, sy2
        try:
            rs[-2].remove()
        except:
            pass
        # Rect = [ [ [x1,x2], [y1,y1] ],
        #         [ [x2,x2], [y1,y2] ],
        #         [ [x1,x2], [y2,y2] ],
        #         [ [x1,x1], [y1,y2] ] ]
        # print(Rect[0][0])
        sx1 = x1
        sx2 = x2
        sy1 = y1
        sy2 = y2
        ix1, ix2 = sorted([x1,x2])
        iy1, iy2 = sorted([y1,y2])
        width = abs(ix2-ix1)
        height = abs(iy2-iy1)
        rs.append(patches.Rectangle(xy=(ix1, iy1), width=width, height=height, ec='#000000', fill=False))
        ax.add_patch(rs[-1])
        
        
        #draw_count += 1
        # for i, rect in enumerate(Rect):
        #     #lns[i].set_data(rect[0],rect[1])
        #     ln, = plt.plot(rect[0],rect[1],color="r",lw=2)
            
        # for rect in Rect:
        #     ln, = plt.plot(rect[0],rect[1],color='r',lw=2)
        #     lns.append(ln)
        #     plt.show()
        
    def mouse_dragged_motion(event):
        plt.title("Now selecting..")
        global x1,y1,x2,y2,DragFlag,r

        # ドラッグしていなければ終了
        if DragFlag == False:
            return

        # 値がNoneなら終了
        if (event.xdata is None) or (event.ydata is None):
            return 

        x2 = event.xdata
        y2 = event.ydata

        # ソート
        # x1, x2 = sorted([x1,x2])
        # y1, y2 = sorted([y1,y2])

        # 四角形を更新
        DrawRect(x1,x2,y1,y2)

        # 描画
        plt.draw()
        if 1 < len(rs):
            for i in range(len(rs)):
                try:
                    Artist.remove(rs[-2])
                    del rs[-2]
                except:
                    pass
        
    # 離した時
    def Release(event):
        plt.title("Right click to verify if this select is fine or select the peak again!")
        global DragFlag
        global is_released
        # フラグをたおす
        DragFlag = False
        is_released = True
        
    
    fig = plt.figure()
    ax = fig.add_subplot()
    plt.title("Please click the top of the peak! :)")
    plt.connect('button_press_event', button_pressed_motion)
    plt.connect("button_release_event", Release)
    plt.connect("motion_notify_event", mouse_dragged_motion)
    plt.scatter(x_list, y_list, s=2)
    plt.show()
    
    #data = reset_range(data_origin, 1600)
    findpeaks = find_peaks(data)
    
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
    
    peaks = []
    
    for i in range(len(x_peaks)):
        
        peaks.append([x_peaks[i], y_peaks[i], bands[i]])
        
        print(f"Fitting result #{i+1}")
        print("-"*30)
        print("x y bandwidth (your guess)")
        print(x_peaks[i], y_peaks[i], bands[i])
        print("x y bandwidth (Fitting result)")
        print(findpeaks.peakxs[i], findpeaks.peakys[i], findpeaks.peakwidth[i])
        print("-"*30)
    
    plt.show()
    
    peaks = pd.DataFrame(peaks, columns=["x", "y", "width"])
    return peaks
    
def seeSpectrum(data):
    
    x_list = data.x
    y_list = data.y
    
    plt.title("")
    plt.scatter(x_list, y_list, s=2)
    plt.show()
    
if __name__ == "__main__":
    
    base_url = "sample_data/"
    endpoint = "sample04.csv"
    
    # x_list = []
    # y_list = []
    # with open(base_url+endpoint, 'r', newline='') as file:
    #     csv_val = csv.reader(file, delimiter=',')
    #     for row in csv_val:
    #         x_list.append(float(row[0]))
    #         y_list.append(float(row[1]))
    
    data= read_data(base_url + endpoint, 0, ',')
    
        
    plot_test(data)
