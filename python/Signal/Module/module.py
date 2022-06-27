from abc import ABCMeta, abstractclassmethod, abstractmethod

class Generator(metaclass=ABCMeta):
    """
    # Parent class of the simluated signal generator
    every simluated signal generator has to inherit Generator as its parent class, thus newly created classes must have these methods below.  
    - add_baseline
    - add_noise
    - add_peaks
    - add_filter (can be a smoother of the baseline or noise low pass filter or something type deal.)
    """
    
    def __init__(self) -> None:
        pass
    
    @abstractmethod
    def add_baseline(self):
        pass
    
    @abstractmethod
    def add_noise(self):
        pass
    
    @abstractmethod
    def add_peaks(self):
        pass

    @abstractmethod
    def add_filter(self):
        pass
    
    def relocated_peaks(self, pos_list, sigma_list):
        if len(pos_list) <= 1:
            return pos_list
        
        for i in range(len(pos_list)):
            for j in range(len(pos_list)):
                # print(pos_list[j] - sigma_list[j], pos_list[i], pos_list[j] + sigma_list[j])
                if i != j and pos_list[j]-4*sigma_list[j] < pos_list[i] < pos_list[j] + 4*sigma_list[j]:
                    if pos_list[i] < pos_list[j]:
                        pos_list[i] = pos_list[j] - 10*sigma_list[j]
                    else:
                        pos_list[i] = pos_list[j] + 10*sigma_list[j]
            if pos_list[i] < 0:
                pos_list[i] = 0
        return pos_list
