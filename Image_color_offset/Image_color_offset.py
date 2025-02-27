"""
檔案名稱: Image_color_offset.py
語言版本: Python 3.12
編譯器/執行環境: MacOS

描述:
影像處理，特效，色差效果

作者: JIK JHONG
日期: 2025.02.27
更新日期: 2025.02.27

版本: v1.0

參考文獻或相關連結:

"""
import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import os
import math

FILE_NAME = "OpenCV_logo_black2.jpeg"
FILE_NAME_NEW = FILE_NAME.split(".")[0] + "_modifed"
FILE_NAME_TYPE = FILE_NAME.split(".")[1]

# RGB 偏移量設定 (R - OFFSET , G , B + OFFSET)
OFFSET = 5 

input = cv.imread(FILE_NAME, cv.IMREAD_UNCHANGED)

def GetImageInfo(input):
    height, width, channel = input.shape
    if channel == 3:
        channel_set = f"RGB({channel})"
    elif channel == 4:
        channel_set = f"RGBA({channel})"
    else:
        channel_set = f"Unknow({channel})"

    print(
        f"Width = {width:,} pixels ,Height = {height:,} pixels ,Channel = {channel_set}"
    )
    print(f"Ratio = {(width / height):.2f}")
    print(f"Size = {input.size:,} pixels")
    print(f"dtype = {input.dtype}")
    print(f"---------")

def filter_channel(input, option="red"):
    height, width, channels = input.shape
    
    if channels < 3:
        print("影像不是彩色的，無法過濾特定顏色通道")
        return
    
    output = np.zeros((height, width, channels), dtype='uint8')
    
    if option == "red":
        channel_set = 2
    elif option == "green":
        channel_set = 1
    elif option == "blue":
        channel_set = 0
    else:
        print("無效的選項，請選擇 'red', 'green' 或 'blue'")
        return
    
    output[:, :, channel_set] = input[:, :, channel_set]  # 只保留指定通道
    return output

def color_offset(input, offset=5):
    input_r = filter_channel(input,"red")
    input_g = filter_channel(input,"green")
    input_b = filter_channel(input,"blue")
    height, width, channels = input.shape
    output = input.copy()
    
    # 確保 offset 合理
    if offset >= height or offset >= width:
        print("Offset 太大，請減小 offset 值")
        return
    
    # 進行顏色偏移
    for j in range(offset, height - offset):
        for i in range(offset, width - offset):  
            output[j, i, 2] = input_r[j - offset, i - offset,2]   
            output[j, i, 1] = input_g[j, i,1]  
            output[j, i, 0] = input_b[j + offset, i + offset,0]  

    cv.imwrite(
            f"{FILE_NAME_NEW}.{FILE_NAME_TYPE}", output, [cv.IMWRITE_JPEG_QUALITY, 80]
    )  # 存成 jpg
    print(f"存檔 - {FILE_NAME_NEW}.{FILE_NAME_TYPE}")
    cv.imshow("Color Offset", output)
    cv.waitKey(0)  # 等待鍵盤輸入
    cv.destroyAllWindows()  # 關閉視窗



GetImageInfo(input)
color_offset(input,OFFSET)
