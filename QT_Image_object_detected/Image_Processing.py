# This Python file uses the following encoding: utf-8

# if __name__ == "__main__":
#     pass
import numpy as np
import cv2
import matplotlib.pyplot as plt
import imghdr
import os
import math
# from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas  # 確保您導入了這個模組


def ImageEdgeDetect(input,paramters,option="Laplacian"):
    output_img = input.copy()
    output = cv2.cvtColor(input, cv2.COLOR_BGR2GRAY)
    output = cv2.medianBlur(output, 7)                 # 模糊化，去除雜訊
    if option == "Laplacian" :
        output = cv2.Laplacian(output, paramters[0], paramters[1], paramters[2])        # 偵測邊緣
    elif option == "Sobel" :
        output = cv2.Sobel(output, paramters[0], paramters[1], paramters[2], paramters[3], paramters[4])        # 偵測邊緣
    elif option == "Canny" :
        output = cv2.Canny(output, paramters[0], paramters[1])        # 偵測邊緣

    # print(f"FF = {output.shape}")
    height, width, channel = output_img.shape
    for i in range(channel):
        output_img[:,:,i] = output[:,:]
    print(f"FF = {output_img.shape}")
    return output_img


def image_pick_color(image, option="red", force_use=0, low_threshold_set=60):
    # image = cv2.imread(input_image)
    height, width, channels = image.shape

    channel_set = 2
    if option == "red":
        channel_set = 2
    elif option == "green":
        channel_set = 1
    elif option == "blue":
        channel_set = 0

    output = np.zeros_like(image)

    for j in range(height):
        for i in range(width):
            if force_use == 1:
                if image[j, i, channel_set] > low_threshold_set:
                    output[j, i, channel_set] = 255
                else:
                    output[j, i, channel_set] = image[j, i, channel_set]
            else:
                output[j, i, channel_set] = image[j, i, channel_set]

    return output

def image_analysis(image, option="all"):
    # image = cv2.imread(input_image)
    height, width, channels = image.shape

    if option == "all":
        if channels != 1:
            if channels == 3:
                tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif channels == 4:
                tmp = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        else:
            tmp = image

        intensity = np.zeros(256, dtype=int)
        for j in range(tmp.shape[0]):
            for i in range(tmp.shape[1]):
                intensity[tmp[j, i]] += 1


        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(range(256), intensity, color='gray')
        ax.set_xlim([0, 255])
        return fig



    elif option == "div":
        image_intensity_r = image_pick_color(image, "red")
        image_intensity_g = image_pick_color(image, "green")
        image_intensity_b = image_pick_color(image, "blue")

        intensity_r = np.zeros(256, dtype=int)
        intensity_g = np.zeros(256, dtype=int)
        intensity_b = np.zeros(256, dtype=int)

        for j in range(image.shape[0]):
            for i in range(image.shape[1]):
                intensity_r[image_intensity_r[j, i, 2]] += 1
                intensity_g[image_intensity_g[j, i, 1]] += 1
                intensity_b[image_intensity_b[j, i, 0]] += 1


        fig, ax = plt.subplots(figsize=(5, 3))
        ax.bar(range(256), intensity_r, color='red', alpha=0.5, label='Red')
        ax.bar(range(256), intensity_g, color='green', alpha=0.5, label='Green')
        ax.bar(range(256), intensity_b, color='blue', alpha=0.5, label='Blue')
        ax.set_xlim([0, 255])
        return fig

    else:
        if channels != 1:
            if channels == 3:
                tmp = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif channels == 4:
                tmp = cv2.cvtColor(image, cv2.COLOR_BGRA2GRAY)
        else:
            tmp = image

        intensity = np.zeros(256, dtype=int)
        for j in range(tmp.shape[0]):
            for i in range(tmp.shape[1]):
                intensity[tmp[j, i]] += 1

        image_intensity_r = image_pick_color(image, "red")
        image_intensity_g = image_pick_color(image, "green")
        image_intensity_b = image_pick_color(image, "blue")

        intensity_r = np.zeros(256, dtype=int)
        intensity_g = np.zeros(256, dtype=int)
        intensity_b = np.zeros(256, dtype=int)

        for j in range(image.shape[0]):
            for i in range(image.shape[1]):
                intensity_r[image_intensity_r[j, i, 2]] += 1
                intensity_g[image_intensity_g[j, i, 1]] += 1
                intensity_b[image_intensity_b[j, i, 0]] += 1



        fig, ax = plt.subplots(figsize=(5, 3))
        ax.fill_between(range(256), intensity, color='gray', alpha=0.8, label='Intensity')
        ax.bar(range(256), intensity_r, color='red', alpha=0.5, label='Red')
        ax.bar(range(256), intensity_g, color='green', alpha=0.5, label='Green')
        ax.bar(range(256), intensity_b, color='blue', alpha=0.5, label='Blue')
        ax.set_xlim([0, 255])

        return fig


def object_detected(image, threshod=80, detect_size=5):
    save_div_image=False
    # 讀取影像
    # copy_set = image.copy()
    # cv2.imshow("Original Image", copy_set)

    # 轉為灰階
    img_with_contours_b = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # 形態學開運算
    kernel_size = detect_size
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_size, kernel_size))
    img_with_contours_b = cv2.morphologyEx(img_with_contours_b, cv2.MORPH_OPEN, kernel)

    # 閾值處理
    _, img_with_contours_b = cv2.threshold(img_with_contours_b, threshod, 255, cv2.THRESH_BINARY)

    # 找出輪廓
    contours, _ = cv2.findContours(img_with_contours_b, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    img_with_contours = image.copy()
    cv2.drawContours(img_with_contours, contours, -1, (0, 255, 0), 4)  # 畫出綠色輪廓

    # 建立遮罩影像
    mask_image = np.zeros(image.shape[:2], dtype=np.uint8)
    for i in range(1, len(contours)):
        cv2.drawContours(mask_image, contours, i, 255, cv2.FILLED)

    # 建立結果影像，只保留輪廓內的內容
    result = np.full_like(image, (255, 255, 255), dtype=np.uint8)
    # image.copyTo(result, mask_image)
    result = cv2.bitwise_and(result, result, mask=mask_image)

    # 標記與裁剪輪廓區域
    for i in range(1, len(contours)):
        shift_mesh = 10
        rect = cv2.boundingRect(contours[i])
        text = str(i)
        text_pos = (rect[0], rect[1] - shift_mesh)
        cv2.putText(result, text, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 0, 0), 2)

    return result , (len(contours) - 1)