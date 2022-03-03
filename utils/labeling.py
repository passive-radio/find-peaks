from re import X
import matplotlib.pyplot as plt

'''
This module aim to put labels on the train data.
'''

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


class put_labels(object):
    def __init__(self, data, mode="click") -> None:
        self.mode = mode
        self.data = data
    
    def by_click(self):
        data = self.data
        
        
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
            global x
            global y
            
            
            #[event] event.button
            # value | info
            #   1   |   left-click
            #   2   |   mouse wheeling
            #   3   |   right-click
            
            if (event.xdata is  None) or (event.ydata is  None):
                return
            
            if event.button == 1:
                x = event.xdata
                y = event.ydata
                
                plt.title(f"peak selected! at ({int(x)},{int(y)})")
                #texts.append(ax.text(100, 30, "Next, Please select the bandwidth by clicking the edge of the peak! (left->right)"))
                
            if event.button == 3:
                x_peaks.append(x)
                y_peaks.append(y)
                plt.title(f"peak pos saved!")
                peak_count += 1
                
            plt.draw()
        
        fig = plt.figure()
        ax = fig.add_subplot()
        plt.title("Please click the top of the peak! :)")
        plt.connect('button_press_event', button_pressed_motion)
        plt.scatter(x_list, y_list, s=2)
        plt.show()
        
        return x_peaks, y_peaks
        
        
    def by_drag(self):
        data = self.data
        
        
        
    def put_labels(self):
        if self.mode == "click":
            return self.by_click()
        
        elif self.mode == "drag":
            return self.by_drag()