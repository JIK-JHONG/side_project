"""
檔案名稱: Image_color_offset_mv.py
語言版本: Python 3.12
編譯器/執行環境: MacOS

描述:
影像(Video)處理，特效，色差效果

作者: JIK JHONG
日期: 2025.02.27
更新日期: 2025.02.27

版本: v1.0

參考文獻或相關連結:

"""
import numpy as np
import cv2 as cv
from tqdm import tqdm

VIDEO_FILE_NAME = "IMG_1383.MOV"
VIDEO_FILE_NAME_NEW = VIDEO_FILE_NAME.split(".")[0] + "_modifed"
VIDEO_FILE_NAME_TYPE = VIDEO_FILE_NAME.split(".")[1]

# RGB 偏移量設定 (R - OFFSET , G , B + OFFSET)
OFFSET = 5 


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
    return output

def VideoLoad(filepath):
    output = cv.VideoCapture(filepath)
    if output is None :
        print("Can't load the video file.")
    else:
        return output



input_video = VideoLoad(VIDEO_FILE_NAME)
frame_width = int(input_video.get(cv.CAP_PROP_FRAME_WIDTH))
frame_height = int(input_video.get(cv.CAP_PROP_FRAME_HEIGHT))
fps = input_video.get(cv.CAP_PROP_FPS)

fourcc = cv.VideoWriter_fourcc(*'avc1')  # H.264 (VideoToolbox) 用 'avc1' 標籤
output_video = cv.VideoWriter(f'{VIDEO_FILE_NAME_NEW}_h264E.mp4', fourcc, fps, (frame_width, frame_height))
total_frames = int(input_video.get(cv.CAP_PROP_FRAME_COUNT))

frame_counter = 0 
pbar = tqdm(total=total_frames, desc="Processing", ncols=100)
while True:
    ret, frame = input_video.read()             # 讀取影片的每一幀
    if not ret:
        print("Cannot receive frame")   # 如果讀取錯誤，印出訊息
        break
    # 影片的幀寬、高度、幀率
    processed_frame = color_offset(frame,OFFSET)
    frame_counter += 1
    pbar.update(1)   # 每次迴圈進行一次進度更新
    output_video.write(processed_frame)
    # cv.imshow('oxxostudio', processed_frame)     # 如果讀取成功，顯示該幀的畫面
    # if cv.waitKey(1) == ord('q'):      # 每一毫秒更新一次，直到按下 q 結束
        # break


pbar.close()
input_video.release()
output_video.release()
cv.destroyAllWindows()
