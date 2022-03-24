# <b>Find Peaks</b>
Python library for identifying the peaks using wavelet transformation.

## <b>Features</b>

1. Peak identification by wavelet transform

    - An example of output  
        ![an example of output](img/wavelet_detection.png)
        (each areas nested in blue are detected peaks)

1. Simulated spectrum dataset generation

1. Peak identification for labeling existing data on GUI

    You can obtain x,y of each peaks on each spectrums by [interactive.py](interactive.py)

    ### Available method
    - click (click the top and the both edges of each peaks)
    - drag (wrap up each peaks)

    ### An example of labelling right peak positons by mouse dragging
    ![labelling by mouse dragging](img/labelling_1.png)
    ![plotted label](img/labelling_2.png)  (each labelled peaks are fitted by gaussian function)

## <b>Future Updates</b>

- <b>Peak identification using CNN(Convolutional Neural Network) and wavelet</b>

    we will reformulate the current approach by wavelet transform as a trainable CNN to increase its detection accuracy and generalization.

- <b>GUI application</b>

    After our peak identification algorhythms gain its enough accuracy and generalization to unseen data, then we will make GUI application that enables you to analyze spectrum data without coding anything.