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
dirJsl = "F:\shuju\jsl"#降水量文件夹路径
dirYmj = "F:\shuju\ymj"#叶面积文件夹路径
arcpy.CheckOutExtension("Spatial")#使用 CheckInExtension 函数将许可归还给许可管理器，以便其他应用程序使用
files = os.listdir(dirJsl)#获取降水量文件夹下所有的文件
for file in files:#遍历文件
    if file.endswith('tif'):#判断是否为tif文件
        if not(os.path.exists('F:/temp')):#判断'F:/temp'零时文件夹路径是否存在
            os.makedirs('F:/temp')#不存在则创建零时文件夹
        if not(os.path.exists('F:/out')):#判断输出文件夹是否存在
            os.makedirs('F:/out')#不存在则创建输出文件夹
        name = file.decode("gbk").encode("utf-8")#吧文件名转成UTF-8编码
        jslFullName = dirJsl+"\\" + name#降水量的tif文件
        ymjFullName = dirYmj+"\\"+name[:6]+"_clip_001.tif"#叶面积的tif文件
        rasterJsl = arcpy.RasterToFloat_conversion(jslFullName)#叶面积的tif文件转成float以便计算
        rasterYmj = arcpy.RasterToFloat_conversion(ymjFullName)
        print "开始计算"
        arcpy.Times_3d(0.17,rasterJsl,"F:/temp/1.tif")
        raster1 = arcpy.RasterToFloat_conversion("F:/temp/1.tif")
        arcpy.Times_3d(0.35,rasterYmj,"F:/temp/2.tif")
        raster2 = arcpy.RasterToFloat_conversion("F:/temp/2.tif")
        arcpy.Times_3d(0.35,rasterYmj,"F:/temp/3.tif")
        raster3 = arcpy.RasterToFloat_conversion("F:/temp/3.tif")
        arcpy.Divide_3d(rasterJsl,raster3,"F:/temp/4.tif")
        raster4 = arcpy.RasterToFloat_conversion("F:/temp/4.tif")
        arcpy.Times_3d(-1,raster4,"F:/temp/5.tif")
        raster5 = arcpy.RasterToFloat_conversion("F:/temp/5.tif")
        expData = arcpy.sa.Exp(raster5)
        expData.save("F:/temp/6.tif")
        raster6 = arcpy.RasterToFloat_conversion("F:/temp/6.tif")
        arcpy.Minus_3d(1,raster6,"F:/temp/7.tif")
        raster7 = arcpy.RasterToFloat_conversion("F:/temp/7.tif")
        arcpy.Times_3d(raster2,raster7,"F:/temp/8.tif")
        raster8 = arcpy.RasterToFloat_conversion("F:/temp/8.tif")
        arcpy.Plus_3d(raster8,raster1,"F:/temp/9.tif")
        if (os.path.exists("F:/out/zbzl"+name[:6]+".tif")):
             os.remove("F:/out/zbzl"+name[:6]+".tif")
        shutil.copyfile("F:/temp/9.tif", "F:/out/zbzl"+name[:6]+".tif")#吧最后的计算结果复制到输出文件夹
        print "计算好了"
        del expData#删除变量引用
        del raster7#删除变量引用
        shutil.rmtree("F:/temp")#请控零时文件夹
if __name__ == '__main__':
    pass
