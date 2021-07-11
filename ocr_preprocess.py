from PIL import Image as PILImage
#import pyocr
import cv2
from PIL.ExifTags import TAGS
from pprint import pprint
import numpy as np
import math
from scipy import ndimage


# コントラスト調整
def adjust(img, alpha=1.0, beta=0.0):
    dst = alpha * img + beta # 積和演算を行う。
    return np.clip(dst, 0, 255).astype(np.uint8) # [0, 255] でクリップし、uint8 型にする。


# 画像の傾き検出
def rotate_img(img):
    l_img = img.copy()
    gray_image = cv2.cvtColor(l_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray_image,50,150,apertureSize = 3)
    minLineLength = 200
    maxLineGap = 30
    lines = cv2.HoughLinesP(edges,1,np.pi/180,100,minLineLength,maxLineGap)

    sum_arg = 0;
    count = 0;
    for line in lines:
        for x1,y1,x2,y2 in line:
            arg = math.degrees(math.atan2((y2-y1), (x2-x1)))
            HORIZONTAL = 0
            DIFF = 20 # 許容誤差 -> -20 - +20 を本来の水平線と考える
            if arg > HORIZONTAL - DIFF and arg < HORIZONTAL + DIFF : 
                sum_arg += arg;
                count += 1

    if count == 0:
        return ndimage.rotate(img, HORIZONTAL)
    else:
        return ndimage.rotate(img, (sum_arg / count) - HORIZONTAL)


# 二値化、大津の二値化
def binary(img, th):
    _img = img.copy()
    _img = np.minimum(_img // th, 1) * 255
    #_img = np.maximum(_img // th, 1)# * 255
    return _img.astype(np.uint8)


def otsu_thresh(img):
    max_vari = -1
    max_th = 0
    for th in range(1, 254):
        m0 = img[img <= th].mean() # mean class 0
        m1 = img[img > th].mean() # mean class 1
        w0 = img[img <= th].size # pixel num class 0
        w1 = img[img > th].size # pixel num class 1
        vari = w0 * w1 / ((w0 + w1) ** 2) * ((m0 - m1) ** 2) # inter class variance
        if vari > max_vari:
            max_th = th
            max_vari = vari
            
    img = binary(img, max_th)
            
    return max_th, img


# グレースケール化
def rgb2gray(img):
    _img = img.copy().astype(np.float32)
    gray = _img[..., 0] * 0.2126 + _img[..., 1] * 0.7152 + _img[..., 2] * 0.0722
    gray = np.clip(gray, 0, 255)
    return gray.astype(np.uint8)


#openpyxlの列名変換
def toAlpha2(num):
    i = int((num-1)/26)
    j = int(num-(i*26))
    Alpha = ''
    for z in i,j:
        if z != 0:
            Alpha += chr(z+64)
    return Alpha