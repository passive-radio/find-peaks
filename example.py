from core.preprocessing import read_data, reset_range
from core.interactive import click_guess, drag_guess
from utils.visualize import see_spectrum

if __name__ == "__main__":
    
    base_url = "sample_data/"
    endpoint = "sample04.csv"

    
    data= read_data(base_url + endpoint, 0, ',')
    
    # select the peak pos by mouse dragging and wrapping each peaks
    peaks = drag_guess(data, background=0, ci=2)
    
    # output_url = "output/"
    # filename, ext = os.path.splitext(endpoint)
    
    # peaks.to_pickle(output_url+filename+"_peaks.pkl")
    # peaks.to_csv(output_url+filename+"_peaks.csv", sep=",")
    