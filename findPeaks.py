import numpy as np
import csv
import pandas as pd
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import matplotlib.cm as cm


class findPeaks(object):
    def __init__(self, data, peaks=None) -> None:
        if type(peaks) == int:
            self.peaks = peaks
        else:
            self.peaks = None
        self.data = data
        
    @property
    def returnPeakNumber(self):
        return int(self.peaks)
    
    def plynomi_func_fit(self, *params, deg, mode="g"):
        x = self.data.x
        
        if mode=="g":
            params_raw = params
            params_guess = params[0:-1]
            #params_guess = [pos, amp, pos, amp,..., bg]
            
            num_func = int(len(params_guess)/2)
            
            params_new = []
            for i in range(num_func):
                params_temp = []
                for j in range(deg):
                    #[pos, amp]
                    params_new.append(params_guess[2*i])
                    params_new.append(params_guess[2*i+1])
            params_new.append(params_raw[-1])

            def plynomi_func(x=x, *params_guess):
                # params_guess = [[pos, amp1, pos, amp2],[pos, amp1, pos, amp2],...]
                if type(params_guess)==list:
                    params = params_guess
                elif type(params_guess)==tuple:
                    params = list(params_guess)
                # return params
                num_func = int((len(params)-1)/(deg*2))
                y_list = []
                for i in range(num_func):
                    y = np.zeros_like(x)
                    for j in range(i, deg):
                        # params[2+deg*i + 2*j+1]       amp
                        # params[2+deg*i + 2*j]         pos
                        # j+1                           deg
                        y = y + np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
                    y_list.append(y)
                
                # for i in range(num_func):
                #     y = np.zeros_like(x)
                #     for j in range(len(params[i])):
                #         print(params[i][j][1])
                #         y = y + np.array(params[i][j][1] * (x-params[i][j][0]) ** (j+1), dtype="float64")
                #     y_list.append(y)
                    
                y_sum = np.zeros_like(x)
                for i in y_list:
                    y_sum = y_sum + i
                    
                #最後にバックグラウンドを追加。
                y_sum = y_sum + params[-1]
                return y_sum
            
            # return plynomi_func(x, params_new)
            popt, pcov = curve_fit(plynomi_func, x, self.data.y, p0=params_new)
            self.popt = popt
            self.pcov = pcov
            return popt, pcov
        
        elif mode=="f":
            params = params
            # params_guess = [[pos, amp1, pos, amp2],[pos, amp1, pos, amp2],...]
            # return params
            num_func = int((len(params)-1)/(deg*2))
            y_list = []
            for i in range(num_func):
                y = np.zeros_like(x)
                for j in range(i, deg):
                    # params[2+deg*i + 2*j+1]       amp
                    # params[2+deg*i + 2*j]         pos
                    # j+1                           deg
                    y = y + np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
                y_list.append(y)
            
            y_sum = np.zeros_like(x)
            for i in y_list:
                y_sum = y_sum + i
                
            #最後にバックグラウンドを追加。
            y_sum = y_sum + params[-1]
            return y_sum
        
    def exp_func_fit(self, *params, mode="g"):
        x = self.data.x
        
        if mode=="g":
            def exp_func(x=x, *params_guess):
                params = params_guess
                #paramsの長さでフィッティングする関数の数を判別。
                num_func = int(len(params)/3)

                #ガウス関数にそれぞれのパラメータを挿入してy_listに追加。
                y_list = []
                for i in range(num_func):
                    y = np.zeros_like(x)
                    param_range = list(range(3*i,3*(i+1),1))
                    ctr = params[int(param_range[0])]
                    amp = params[int(param_range[1])]
                    wid = params[int(param_range[2])]
                    y = y + amp * np.exp( -((x - ctr)/wid)**2)
                    y_list.append(y)

                #y_listに入っているすべてのガウス関数を重ね合わせる。
                y_sum = np.zeros_like(x)
                for i in y_list:
                    y_sum = y_sum + i

                #最後にバックグラウンドを追加。
                y_sum = y_sum + params[-1]

                return y_sum
            
            popt, pcov = curve_fit(exp_func, x, self.data.y, p0=params)
            self.popt = popt
            self.pcov = pcov
            return popt, pcov
        
        elif mode=="f":
            #paramsの長さでフィッティングする関数の数を判別。
            num_func = int(len(params)/3)

            #ガウス関数にそれぞれのパラメータを挿入してy_listに追加。
            y_list = []
            for i in range(num_func):
                y = np.zeros_like(x)
                param_range = list(range(3*i,3*(i+1),1))
                ctr = params[int(param_range[0])]
                amp = params[int(param_range[1])]
                wid = params[int(param_range[2])]
                y = y + amp * np.exp( -((x - ctr)/wid)**2)
                y_list.append(y)

            #y_listに入っているすべてのガウス関数を重ね合わせる。
            y_sum = np.zeros_like(x)
            for i in y_list:
                y_sum = y_sum + i

            #最後にバックグラウンドを追加。
            y_sum = y_sum + params[-1]

            return y_sum
            
    def exp_fit_plot(self,*params):
        x = self.data.x
        num_func = int(len(params)/3)
        y_list = []
        for i in range(num_func):
            y = np.zeros_like(x)
            param_range = list(range(3*i,3*(i+1),1))
            ctr = params[int(param_range[0])]
            amp = params[int(param_range[1])]
            wid = params[int(param_range[2])]
            y = y + amp * np.exp( -((x - ctr)/wid)**2) + params[-1]
            y_list.append(y)
        return y_list
    
    def fit_plot(self, *params, func="exp", deg=None):
        x = self.data.x
        y = self.data.y
        
        if func=="exp":
            num_func = int(len(params)/3)
            y_list = []
            fit = self.exp_func_fit(*params, mode="f")
            plt.scatter(x, y, s=20)
            plt.plot(x, fit , ls='-', c='black', lw=1)
            
            for i in range(num_func):
                y = np.zeros_like(x)
                param_range = list(range(3*i,3*(i+1),1))
                ctr = params[int(param_range[0])]
                amp = params[int(param_range[1])]
                wid = params[int(param_range[2])]
                y = y + amp * np.exp( -((x - ctr)/wid)**2) + params[-1]
                y_list.append(y)
            
            baseline = np.zeros_like(x) + params[-1]
            for n,i in enumerate(y_list):
                plt.fill_between(x, i, baseline, facecolor=cm.rainbow(n/len(y_list)), alpha=0.6)
                
        if func=="poly":
            
            params = params
            # params_guess = [[pos, amp1, pos, amp2],[pos, amp1, pos, amp2],...]
            # return params
            num_func = int((len(params)-1)/(deg*2))
            # y_list = []
            
            
            # y_sum = np.zeros_like(x)
            # for i in y_list:
            #     y_sum = y_sum + i
                
            # #最後にバックグラウンドを追加。
            # y_sum = y_sum + params[-1]
            # return y_sum
            y_list = []
            fit = self.plynomi_func_fit(*params, mode="f", deg=deg)
            plt.scatter(x, y, s=20)
            plt.plot(x, fit , ls='-', c='black', lw=1)
            
            for i in range(num_func):
                y = np.zeros_like(x)
                for j in range(i, deg):
                    # params[2+deg*i + 2*j+1]       amp
                    # params[2+deg*i + 2*j]         pos
                    # j+1                           deg
                    y = y + np.array(params[2*deg*i + 2*j+1] * (x-params[2*deg*i + 2*j]) ** (j+1), dtype="float64")
                y_list.append(y)
            
            # baseline = np.zeros_like(x) + params[-1]
            # plt.plot(x, baseline, ls='-', c='gray', alpha=0.6, lw=1)
            # for n,i in enumerate(y_list):
            #     plt.fill_between(x, i, baseline, facecolor=cm.rainbow(n/len(y_list)), alpha=0.6)
    
    @property
    def peakxs(self):
        popt = self.popt
        peakxs = [popt[i] for i in range(len(popt)) if i % 3 ==1]
        return peakxs
    
    @property
    def peakwidth(self):
        popt = self.popt
        peakwidth = [popt[i] for i in range(len(popt)) if i % 3 ==2]
        return peakwidth
        
    
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
        print("Error: xrange should be [x_start, x_end]")
        