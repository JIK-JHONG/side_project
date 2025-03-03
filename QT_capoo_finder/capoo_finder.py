from ultralytics import YOLO
import torch
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import imghdr
import os
import math
from pathlib import Path


# 檢查是否支援 MPS（Mac Metal）
def Apple_Silicon_Support():
    if torch.backends.mps.is_available():
        print("Using MPS for computation.")
        return True
    else:
        print("MPS not available, using CPU.")
        return False

# 檢查是否支援 CUDA（NVIDIA GPU）
def CUDA_Support():
    if torch.cuda.is_available():
        print("Using CUDA for computation.")
        return True
    else:
        print("CUDA not available, using CPU.")
        return False

def check_hardware_for_ML():
    if (Apple_Silicon_Support()):
        return 2
    else:
        if (CUDA_Support()):
            return 1
        else:
            return 0


def capoo_finder_tool(input,relability=60,hardware_accelerate=True):
    relability = relability / 100.0
    print(f"relability = {relability}")
    class_info = ["Capoo","DogDog"]
    class_cal = [0,0]
    # (229, 200, 141), (82, 180, 248),
    color_table = [
        (255, 0, 0), (255, 4, 0), (255, 8, 0), (255, 12, 0), (255, 16, 0),
        (255, 20, 0), (255, 24, 0), (255, 28, 0), (255, 32, 0), (255, 36, 0),
        (255, 40, 0), (255, 44, 0), (255, 48, 0), (255, 52, 0), (255, 56, 0),
        (255, 60, 0), (255, 64, 0), (255, 68, 0), (255, 72, 0), (255, 76, 0),
        (255, 80, 0), (255, 84, 0), (255, 88, 0), (255, 92, 0), (255, 96, 0),
        (255, 100, 0), (255, 104, 0), (255, 108, 0), (255, 112, 0), (255, 116, 0),
        (255, 120, 0), (255, 124, 0), (255, 128, 0), (255, 132, 0), (255, 136, 0),
        (255, 140, 0), (255, 144, 0), (255, 148, 0), (255, 152, 0), (255, 156, 0),
        (255, 160, 0), (255, 164, 0), (255, 168, 0), (255, 172, 0), (255, 176, 0),
        (255, 180, 0), (255, 184, 0), (255, 188, 0), (255, 192, 0), (255, 196, 0),
        (255, 200, 0), (255, 204, 0), (255, 208, 0), (255, 212, 0), (255, 216, 0),
        (255, 220, 0), (255, 224, 0), (255, 228, 0), (255, 232, 0), (255, 236, 0),
        (255, 240, 0), (255, 244, 0), (255, 248, 0), (255, 252, 0), (255, 255, 0),
        (252, 255, 0), (248, 255, 0), (244, 255, 0), (240, 255, 0), (236, 255, 0),
        (232, 255, 0), (228, 255, 0), (224, 255, 0), (220, 255, 0), (216, 255, 0),
        (212, 255, 0), (208, 255, 0), (204, 255, 0), (200, 255, 0), (196, 255, 0),
        (192, 255, 0), (188, 255, 0), (184, 255, 0), (180, 255, 0), (176, 255, 0),
        (172, 255, 0), (168, 255, 0), (164, 255, 0), (160, 255, 0), (156, 255, 0),
        (152, 255, 0), (148, 255, 0), (144, 255, 0), (140, 255, 0), (136, 255, 0),
        (132, 255, 0), (128, 255, 0), (124, 255, 0), (120, 255, 0), (116, 255, 0),
        (112, 255, 0), (108, 255, 0), (104, 255, 0), (100, 255, 0), (96, 255, 0),
        (92, 255, 0), (88, 255, 0), (84, 255, 0), (80, 255, 0), (76, 255, 0),
        (72, 255, 0), (68, 255, 0), (64, 255, 0), (60, 255, 0), (56, 255, 0),
        (52, 255, 0), (48, 255, 0), (44, 255, 0), (40, 255, 0), (36, 255, 0)
    ]


    # 確認是否支援 MPS
    print(f"cc++hardware_accelerate = {hardware_accelerate}")
    if Apple_Silicon_Support() and hardware_accelerate:
        device = torch.device("mps")  # 使用 MPS
        print("Using MPS for computation.")
    elif CUDA_Support():
        device = torch.device("cuda")  # 使用 CUDA
        print("Using CUDA for computation.")
    else:
        device = torch.device("cpu")  # 使用 CPU
        print("Using CPU for computation.")


    # 載入訓練好的模型

    # 取得當前 Python 腳本的絕對路徑
    script_dir = Path(__file__).resolve().parent

    # 設定 YOLO 模型的正確路徑
    model_path = script_dir / "core/capoo/capoo_dogdog_training/weights/best.pt"

    # 載入模型
    model = YOLO(str(model_path))

    # 轉移到裝置（GPU 或 CPU）
    # device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    # model = YOLO("capoo/capoo_dogdog_training/weights/best.pt")


    model.to(device)
    # 預測單張圖片
    start_time = time.time()
    # results = model(FILE_NAME)
    # frame = cv2.imread(FILE_NAME)
    # frame = cv2.imread(FILE_NAME)
    frame = cv2.cvtColor(input, cv2.COLOR_BGR2RGB)
    # frame_marked = input ;
    results = model(frame)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"物體偵測耗時: {round(elapsed_time, 2)} 秒")
    # for result in results:
    #     for box in result.boxes:
    #         cls_id = int(box.cls)
    #         conf = float(box.conf)
    #         print(f"類別 ID: {cls_id}, 置信度: {conf}")
    #     result.show()  # 顯示結果


    print(model.names)

    # 提取每個物件的資訊
    for result in results:
        for box in result.boxes:
            if box.xyxy is None or len(box.xyxy) == 0:
                print("無效的邊界框，跳過")
                continue

            # 展平 xyxy 張量
            xyxy = box.xyxy.view(-1).cpu().numpy().astype(int)  # 或者用 box.xyxy[0].cpu().numpy().astype(int)
            if len(xyxy) != 4:
                print(f"邊界框格式錯誤: {xyxy}")
                continue
            # print("Box:", box)
            # print("Box.xyxy:", box.xyxy)  # 檢查 xyxy 的值
            # 解包
            x1, y1, x2, y2 = xyxy
            cls_id = int(box.cls)
            conf = float(box.conf)
            if (conf > relability ):
                print(f"類別 ID: {cls_id} {model.names[cls_id]}, 置信度: {conf}, 邊界框: {xyxy}")
                cv2.rectangle(frame, (x1, y1), (x2, y2), color_table[cls_id], 2)
                cv2.rectangle(frame, (x1, y1-40), (x2, y1), color_table[cls_id], -1)
                cv2.putText(frame, f"{model.names[cls_id]}: {conf:.2f}", (x1 + 2, y1 - 10 + 2),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                cv2.putText(frame, f"{model.names[cls_id]}: {conf:.2f}", (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
                print(f"類別 ID: {cls_id} {model.names[cls_id]}, 置信度: {conf:.4f}, 邊界框: {xyxy}")
                class_cal[cls_id] += 1



    # output_path = f'{FILE_NAME.split(".")[0]}_modified.jpeg'
    # cv2.imwrite(output_path, frame)
    # print(f"結果已保存至: {output_path}")
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    result_summary = {}
    for i in range(len(class_cal)):
        print(f"{class_info[i]} = {class_cal[i]} set\n")
        result_summary[class_info[i]] = class_cal[i]


    return frame, result_summary,round(elapsed_time, 2)




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
        # ax.set_title("Gray Intensity Distribution")
        # ax.set_xlabel("Pixel Value")
        # ax.set_ylabel("Frequency")

        # **轉換 Matplotlib 圖表為 QImage**
        # canvas = FigureCanvas(fig)
        # canvas.draw()
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
        # ax.set_title("RGB Intensity Distribution")
        # ax.set_xlabel("Pixel Value")
        # ax.set_ylabel("Frequency")

        # **轉換 Matplotlib 圖表為 QImage**
        # canvas = FigureCanvas(fig)
        # canvas.draw()
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
        # ax.set_title("RGB + Intensity Distribution")
        # ax.set_xlabel("Pixel Value")
        # ax.set_ylabel("Frequency")

        # **轉換 Matplotlib 圖表為 QImage**

        return fig



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
