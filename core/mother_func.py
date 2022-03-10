import math
import numpy as np

"""
## mother functions

- Poisson wavelet
- Morlet wavelet
- Modified Morlet wavelet
- Mexican hat wavelet
- Complex Mexican hat wavelet
- Shannon wavelet
- Meyer wavelet
- Difference of Gaussians
- Hermitian wavelet
- Beta wavelet
- Causal wavelet
- μ wavelets
- Cauchy wavelet
- Addison wavelet

"""

# マザーウェーブレット：モルレーウェーブレット
def morlet_func(x, f, width):
    sf = f / width
    st = 1 / (2 * math.pi * sf)
    A = 1 / (st * math.sqrt(2 * math.pi))
    h = -np.power(x, 2) / (2 * st**2)
    co1 = 1j * 2 * math.pi * f * x
    return A * np.exp(co1) * np.exp(h)

def haar_func():
    return

    
def mexican_hat_func():
    return
