from findPeaks import read_data, reset_range
from interactive import plot_test, seeSpectrum
from bmpToCSV import bmpToCSV

if __name__ == "__main__":
    
    base_url = "sample_data/"
    endpoint = "sample03.bmp"
    file_path = base_url + endpoint
    
    bmpToCSV(file_path)
    
    endpoint = "sample03.csv"
    
    # x_list = []
    # y_list = []
    
    # with open(base_url+endpoint, 'r', newline='', encoding="utf-8") as file:
    #     csv_val = csv.reader(file, delimiter=',')
    #     for row in csv_val:
    #         x_list.append(float(row[0]))
    #         y_list.append(float(row[1]))
    
    data= read_data(base_url + endpoint, 0, ',')
    
    #data = reset_range(data, 260, 330)
    plot_test(data)
    #seeSpectrum(data)