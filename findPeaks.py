class findPeaks(object):
    def __init__(self, peaks, data) -> None:
        self.peaks = int(peaks)
        self.data = data
        
    @property
    def returnPeakNumber(self):
        return int(self.peaks)
    
    def reset_range(self, xrange):
        if xrange != None:
            start = xrange[0]
            end = xrange[1]
            return self.data[start:end]
