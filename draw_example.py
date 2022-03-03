from interactive import drag_guess
from utils.draw_test import draw_test

if __name__ == "__main__":
    
    output_dir = 'output/'

    # data = draw(output_dir + "drawed.csv", mode="rd")
    data = draw_test(output_dir + "drawed.csv", mode="rd")
    # select the peak pos by mouse dragging and wrapping each peaks
    peaks = drag_guess(data, background=0, ci=2)