import matplotlib.pyplot as plt

def see_spectrum(data):
    
    x_list = data.x
    y_list = data.y
    
    plt.title("")
    plt.scatter(x_list, y_list, s=2)
    plt.show()
    
def check_dir_spectra(dir_path, num):
    import os
    import pandas as pd
    filelist = os.listdir(dir_path)
    print(filelist[0])
    filelist = sorted(filelist, key=lambda x: int(os.path.splitext(os.path.basename(x))[0][15:]))
    filelist = filelist[:num]
    
    for file in filelist:
        df = pd.read_csv(dir_path + file, sep=",")
        df = df.set_axis(["x", "y"], axis="columns")
        
        plt.scatter(df.x, df.y, s=2)
        plt.show()