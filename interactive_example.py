import csv

from findPeaks import findPeaks, read_data, reset_range
from interactive import plot_test

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