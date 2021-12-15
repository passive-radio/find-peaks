from pandas.core import base
from findPeaks import read_data, reset_range
from interactive import plot_test, seeSpectrum, draw_test
from bmpToCSV import bmpToCSV

if __name__ == "__main__":
    
    base_url = "sample_data/"
    # endpoint = "sample02.bmp"
    # file_path = base_url + endpoint
    
    # bmpToCSV(file_path)
    
    # endpoint = "sample02.csv"
    
    # # x_list = []
    # # y_list = []
    
    # # with open(base_url+endpoint, 'r', newline='', encoding="utf-8") as file:
    # #     csv_val = csv.reader(file, delimiter=',')
    # #     for row in csv_val:
    # #         x_list.append(float(row[0]))
    # #         y_list.append(float(row[1]))
    
    # data= read_data(base_url + endpoint, 0, ',')
    
    # # Support optional number of peaks determination with interactive help
    
    # """
    # left click at the top of the peak -> left click at the both edge of the peak -> [guide] Next, click the top of the next peak! -> ...
    # """
    
    # #data = reset_range(data, 260, 330)
    # plot_test(data)
    # #seeSpectrum(data)
    
    endpoint = "sample.csv"
    
    file_path= base_url + endpoint
    
    data = draw_test(file_path, mode="wrd")
    
    plot_test(data)
    