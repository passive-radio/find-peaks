from decimal import Decimal, ROUND_HALF_UP
import csv
import os

from PIL import Image

def bmpToCSV(file):
    lum_list = []
    pixel_lum = []
    image = Image.open(file)
    image = image.convert("L")
    width, height = image.size
    for x in range(width):
        xlum = 0
        for y in range(height):
            xlum += image.getpixel((x,y))
        xlum = float(Decimal(str(xlum/ height)).quantize(Decimal('0.0001'), rounding=ROUND_HALF_UP))
        pixel_lum.append([x, xlum])
        lum_list.append(xlum)
        
    filename = os.path.splitext(os.path.basename(file))[0]
    dirname = os.path.dirname(file)
    
    try:
        with open(dirname +"/"+ filename + ".csv", 'w', newline='', encoding="utf-8") as file:
            mywriter = csv.writer(file, delimiter=',')
            mywriter.writerows(pixel_lum)
        # print("CSV file successfully generated!")
    except Exception as e:
        print(f"{e}")

if __name__ == "__main__":
    base_path = "../data/atom_linear_spectrum/"
    
    
    for file in os.listdir(base_path):
        bmpToCSV(base_path + file)
    