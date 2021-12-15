from pandas.core import base
from findPeaks import read_data, reset_range
from interactive import click_guess, drag_guess, seeSpectrum, draw_test
from bmpToCSV import bmpToCSV
from pprint import pprint

if __name__ == "__main__":
    
    # base_url = "sample_data/"
    # endpoint = "sample04.bmp"
    # file_path = base_url + endpoint
    
    # bmpToCSV(file_path)
        
    base_url = "sample_data/"
    endpoint = "sample04.csv"

    
    data= read_data(base_url + endpoint, 0, ',')
    
    drag_guess(data)            # select the peak pos by mouse dragging and wrapping each peaks
    click_guess(data)           # select the peak pos by clicking the edge of each peaks