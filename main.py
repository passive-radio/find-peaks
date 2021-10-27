from configparser import MAX_INTERPOLATION_DEPTH
from findPeaks import findPeaks

def main():
    findpeak = findPeaks(1)
    print(findpeak.returnPeakNumber)

if __name__ == "__main__":
    main()