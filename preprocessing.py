import os, sys, subprocess, cv2
from osgeo import gdal,gdalnumeric,gdalconst
from osgeo import gdalconst
import glob
import numpy as np


Tiff_inpath = "...\\" #TIFF path before preprocessing
Tiff_outpath="...\\"  #TIFF path after preprocessing
tif_files = glob.glob(Tiff_inpath + "*.tif")

Nfile=len(tif_files)
ifile=0
for tif_infile in tif_files:
    ifile=ifile+1
    #---Read GeoTiff
    dataset=gdal.Open(tif_infile)
    row=dataset.RasterYSize
    col=dataset.RasterXSize
    geotrans=dataset.GetGeoTransform()
    proj=dataset.GetProjection()
    Info=gdal.Info(tif_infile)
    Nband=dataset.RasterCount
    band=dataset.GetRasterBand(1)  #get band
    data=band.ReadAsArray()
    NoD=band.GetNoDataValue()

    #---morphological opening-and-closing operation
    dataTemp1=data
    kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(5,5)) #kernel size
    #closing operation
    dataTemp2=cv2.morphologyEx(dataTemp1, cv2.MORPH_CLOSE,kernel,iterations=1)
    del dataTemp1
    #opening operation
    datanew=cv2.morphologyEx(dataTemp1, cv2.MORPH_OPEN,kernel,iterations=1)
    del dataTemp2

    #write to GeoTiff
    filename=os.path.basename(tif_infile)
    filename=filename[:-4]
    driver=gdal.GetDriverByName('GTiff')
    outRaster=driver.Create(Tiff_outpath + filename + ".tif",row,col,1,gdal.GDT_Byte,["COMPRESS=LZW"])
    outRaster.SetGeoTransform(geotrans)
    outband=outRaster.GetRasterBand(1)
    outband.WriteArray(datanew)
    outRaster.SetProjection(proj)
    outRaster=None 
    print(filename)

    

