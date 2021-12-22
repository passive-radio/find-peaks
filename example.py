import os
from pprint import pprint

from matplotlib.pyplot import draw
from pandas.core import base

from findPeaks import read_data, reset_range
from interactive import click_guess, drag_guess, seeSpectrum, draw_test
from bmpToCSV import bmpToCSV

if __name__ == "__main__":
    
    # base_url = "sample_data/"
    # endpoint = "sample04.bmp"
    # file_path = base_url + endpoint
    
    # bmpToCSV(file_path)
        
    base_url = "sample_data/"
    endpoint = "sample04.csv"

    
    data= read_data(base_url + endpoint, 0, ',')
    
    # data = draw_test(base_url + "sample.csv", mode="wrd")
    
    # select the peak pos by mouse dragging and wrapping each peaks
    peaks = drag_guess(data, background=0)
    
    print(peaks)
    
    output_url = "output/"
    filename, ext = os.path.splitext(endpoint)
    
    peaks.to_pickle(output_url+filename+"_peaks.pkl")
    peaks.to_csv(output_url+filename+"_peaks.csv", sep=",")
    
    # select the peak pos by clicking the edge of each peaks
    # click_guess(data)