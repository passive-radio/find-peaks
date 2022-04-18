from email import header
from multimethod import distance
import scipy
from scipy.signal import find_peaks as scipy_find
from core.preprocessing import read_data

from scipy.signal._peak_finding_utils import _local_maxima_1d
from scipy.signal._peak_finding import _arg_x_as_expected

from utils.visualize import see_spectrum

if __name__ == "__main__":
    
    data = read_data("sample_data/sample04.csv", headers=0, delimineter=",")
    print(data)
    peaks = scipy_find(x=data.y, prominence=10)
    
    properties = peaks[1]
    peaks = peaks[0]
    print(peaks)
    print(properties)
    
    see_spectrum(data)