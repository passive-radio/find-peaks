class findPeaks(object):
    def __init__(self, peaks=1) -> None:
        self.peaks = int(peaks)
        pass
        
    @property
    def returnPeakNumber(self):
        return int(self.peaks)