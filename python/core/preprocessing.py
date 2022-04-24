import sys
sys.path.append('utils/')
sys.path.append('../')

import matplotlib.pyplot as plt
from to_np_data import to_xy_data, read_xy_data

'''
Preprocsdding module

* normalization
* noise reduction
* baseline correlation
'''

if __name__ == "__main__":
    x_filepath = "../../data/ans_type2_x.npy"
    y_filepath = "../../data/ans_type2_y.npy"
    x_data, y_data = read_xy_data(x_filepath, y_filepath)
    
    plt.imshow(x_data[0])
    plt.show()
    
