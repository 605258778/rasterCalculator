#!/usr/bin/python
# -*- coding:utf8 -*-
import sys
import arcpy
import os
import time
import shutil
from arcpy.sa import *
from decimal import Decimal
reload(sys)
sys.setdefaultencoding('utf-8')
dirJsl = "F:\shuju\jsl"
dirYmj = "F:\shuju\ymj"
arcpy.CheckOutExtension("Spatial")
count = 0
files = os.listdir(dirJsl)
for file in files:
    if file.endswith('tif'):
        countStr = str(count)
        name = file.decode("gbk").encode("utf-8")
        jslFullName = dirJsl+"\\" + name
        ymjFullName = dirYmj+"\\"+name[:6]+"_clip_001.tif"
        rasterJsl = arcpy.RasterToFloat_conversion(jslFullName)
        rasterYmj = arcpy.RasterToFloat_conversion(ymjFullName)
        print "开始"
        arcpy.Times_3d(0.17,rasterJsl,"F:/temp/1"+countStr+".tif")
        raster1 = arcpy.RasterToFloat_conversion("F:/temp/1"+countStr+".tif")
        arcpy.Times_3d(0.35,rasterYmj,"F:/temp/2"+countStr+".tif")
        raster2 = arcpy.RasterToFloat_conversion("F:/temp/2"+countStr+".tif")
        arcpy.Times_3d(0.35,rasterYmj,"F:/temp/3"+countStr+".tif")
        raster3 = arcpy.RasterToFloat_conversion("F:/temp/3"+countStr+".tif")
        arcpy.Divide_3d(rasterJsl,raster3,"F:/temp/4"+countStr+".tif")
        raster4 = arcpy.RasterToFloat_conversion("F:/temp/4"+countStr+".tif")
        arcpy.Times_3d(-1,raster4,"F:/temp/5"+countStr+".tif")
        raster5 = arcpy.RasterToFloat_conversion("F:/temp/5"+countStr+".tif")
        expData = arcpy.sa.Exp(raster5)
        expData.save("F:/temp/6"+countStr+".tif")
        raster6 = arcpy.RasterToFloat_conversion("F:/temp/6"+countStr+".tif")
        arcpy.Minus_3d(1,raster6,"F:/temp/7"+countStr+".tif")
        raster7 = arcpy.RasterToFloat_conversion("F:/temp/7"+countStr+".tif")
        arcpy.Times_3d(raster2,raster7,"F:/temp/8"+countStr+".tif")
        raster8 = arcpy.RasterToFloat_conversion("F:/temp/8"+countStr+".tif")
        arcpy.Plus_3d(raster8,raster1,"F:/temp/9"+countStr+".tif")
        shutil.copyfile("F:/temp/9"+countStr+".tif", "F:/out/zbzl"+name[:6]+".tif")
        print "好了"
        count = count+1

if __name__ == '__main__':
    pass
