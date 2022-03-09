from utils.visualize import see_spectrum
from core.preprocessing import read_data
import numpy as np
import matplotlib.pyplot as plt
file = "../data/proportional_tubes_x_ray/spectrum_type2_0.mca"

data = read_data(file, delimiter=",", headers=11, footers=1031, errors="ignore", contains_x_axis=False)
y = data.y
x = data.x

x = np.array(x).astype(np.int32)
y = np.array(y).astype(np.float32)

data.x = x
data.y = y
plt.scatter(x,y)

plt.show()

data.plot()
plt.show()

# see_spectrum(data)