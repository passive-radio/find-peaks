import sys

sys.path.append('../')
sys.path.append('../core/')

# from core.preprocessing import read_data, reset_range
from core.to_np_data import read_file
from core.fitter_gui import click_guess, drag_guess
from utils.visualize import see_spectrum

if __name__ == "__main__":
    
    base_url = "../sample_data/"
    endpoint = "sample_data.csv"
    
    data= read_file(base_url + endpoint, ",", contains_x_axis=True)
    
    # select the peak pos by mouse dragging and wrapping each peaks
    peaks = drag_guess(data, background=0, ci=2)
    