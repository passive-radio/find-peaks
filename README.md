# <b>find peaks</b>
This project focuses on finding and fitting peaks.
with the help of the GUI fitting method, you can find and fit optional number of peaks.

## <b>Spectrum data format must be like the table below</b>

| x | y |
|---|---|
|0  | 1  |
|1  | 13 |
|2  | 30 |
|3  | 43 |
|4  | 31 |
|5  | 11 |
|...|...|

## <b>Features</b>

1. Peak fitting on GUI window

    Now you can obtain x,y of each peak on the spectrum by using [interactive.py](interactive.py)

    ### Available method
    - click (click the top and both edge of each peaks)
    - drag (wrap up the peak area by mouse dragging)

    ### Click example
    ![interactive peak guessing](img/interactive_step1.png)
    ![selecting another peak](img/interactive_another_peak.png)
    ![results](img/peak_found.png)


2. Converting bmp image files to csv files

    You can directly find and fit peaks from the image(which contains spectrum data) by [interacive.py](interactive.py) without additional hassle of converting bmp images into csv files.

    Notice: file format of the images must be bmp(.bmp, .jpg, .png, .jpeg). Vector format isn't supported.

## <b>Available approximation curve types</b>

- gaussian function
- polynomial function

## <b>Supported supectrum files format </b>
* ascii file(.asc .csv .txt etc..)
* bmp image(.bmp .jpg .png .jpeg etc..)

    excel sheet files, table of html are planed to be suported in the near future.

## <b>Future features</b>

- <b>fully auto peak detection using CNN(Convolutional Neural Network)</b>
- <b>local application(cross platform)</b>
- get the peak positions with its errors 
- baseline correlation
- other fitting function like binomical distribution func