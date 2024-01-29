import os, sys, subprocess, cv2
from osgeo import gdal,gdalnumeric,gdalconst
from osgeo import gdalconst
import glob
import numpy as np


textfile='...\\filelist2020.txt' # tiff list need to be mosaic
fileCont=open(textfile,mode='r',encoding='UTF-8')  #convert to 'UTF-8'
lines=fileCont.readlines() #
# strip()
fileDir = [x.strip() for x in lines]
Tifflist = fileDir #all tiff
#print(Tifflist)

vrtpath='...\VRT\\vrt2020_30m.vrt'
mosicfile='...\MosicResult\\TPwater2020_30m.tif' # output

def compress(path, target_path):
    #"""compress tiff using gdal"""
    dataset = gdal.Open(path)
    driver = gdal.GetDriverByName('GTiff')
    driver.CreateCopy(target_path, dataset, strict=1, callback=progress, options=["TILED=YES", "COMPRESS=LZW","BIGTIFF=YES"])
    # strict=1 strictly the same as before.  0-adjustments area possible
    # PACKBITS  Fast lossless compression based on streams
    # LZW For pixel. better in black and white image
    dataset.FlushCache()
    dataset=None
    del dataset

print('Mosaicing...')
vrtImg=gdal.BuildVRT(vrtpath, Tifflist)
vrtImg.FlushCache()

print('Compress:')
compress(vrtpath,mosicfile)

print('Build pyramid:')
subprocess.call('gdaladdo -ro --config BIGTIFF_OVERVIEW YES ...\\TPwater2020.tif 2 4 8 16 32 64 128')
#replace "..." to the path of output tiff

