import math
import numpy as np
import matplotlib.pyplot as plt

from numpy import uint32

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

class mother_wavelet(object):
    def __init__(self, a, deltab, width=None) -> None:
        
        if width == None:
            scale_space = np.arange(-a/2+deltab/2, a/2+deltab/2, deltab)
            width = a
        else:
            scale_space = np.arange(-width/2+deltab/2, width/2+deltab/2, deltab)
        
        self.a = a
        self.deltab = deltab
        self.width = width
        self.scale_space = scale_space
        self.mother_name = None

    def morlet_func(self, freq, a=None, deltab=None, width=None):
        if a != None:
            self.a = a
        if deltab != None:
            self.deltab = deltab
        if width != None:
            self.width = width
            self.scale_space = np.arange(-width/2+deltab/2, width/2+deltab/2, self.deltab)
        self.mother_name = "morlet"
        wab = np.exp(-np.power(self.scale_space, 2)/np.power(self.a/freq, 2))
        wab = np.power(self.a, -1/2)*wab
        self.wab = wab
        return wab
    
    def LoG_func_old(self, freq, a=None, deltab=None, width=None):
        if a != None:
            self.a = a
        if deltab != None:
            self.deltab = deltab
        if width != None:
            self.width = width
            self.scale_space = np.arange(-width/2+deltab/2, width/2+deltab/2, self.deltab)
        self.mother_name = "morlet"
        
        wab = (1-np.power(self.scale_space,2))*\
                np.exp(-np.power(self.scale_space,2)/self.a)
        wab = np.power(self.a, -1/2)*wab
        self.wab = wab
        return wab
    
    def LoG_func(self, freq, a=None, deltab=None, width=None):
        if a != None:
            self.a = a
        if deltab != None:
            self.deltab = deltab
        if width != None:
            self.width = width
            self.scale_space = np.arange(-width/2+deltab/2, width/2+deltab/2, self.deltab)
        self.mother_name = "LoG"
        
        def g(a):
            return 1/a
        
        wab = g(self.a)*np.power(self.a, -1/2)*(1-np.power(self.scale_space/self.a, 2))*\
            np.exp(-np.power(self.scale_space/self.a, 2)/2)
        self.wab = wab
        return wab
    
    def morlet_func_old(x, f, width):
        st = width / (2 * math.pi) / f
        A = 1 / (st * math.sqrt(2 * math.pi))
        h = -np.power(x, 2) / (2 * st**2)
        co1 = 1j * 2 * math.pi * f * x
        return A * np.exp(co1) * np.exp(h)
    
    def mother_func(self, mother, freq, a=None, deltab=None, width=None):
        
        if mother == "morlet":
            return self.morlet_func(freq, a, deltab, width)
        elif mother == "LoG":
            return self.LoG_func(freq, a, deltab, width)
        
    @property
    def plot_mother(self) -> None:
        fig, axs = plt.subplots(1,1,figsize=(6,4))
        axs.plot(self.wab, label=f"{self.mother_name} W(a,b)")
        axs.legend()
        plt.show()
        return None
    
    @property
    def info(self) -> None:
        print(f"mother func: {self.mother_name}")
        print(f"mother func amp: {self.a}")
        print(f"mother func delta_b: {self.deltab}")
        print(f"mother func width: {self.width}")
        print(f"mother func scale space: {self.scale_space[0]}~{self.scale_space[-1]}")
        return None