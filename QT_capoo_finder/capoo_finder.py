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


# 確認是否支援 MPS
def Apple_Silicon_Support():
    if torch.backends.mps.is_available():
        print("Using MPS for computation.")
        return True
    else:
        print("MPS not available, using CPU.")
        return False


def capoo_finder_tool(input,relability=60):
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

    if (Apple_Silicon_Support()):
        device = torch.device("mps")  # 使用 Metal Performance Shaders
    else:
        device = torch.device("cpu")  # 無 MPS 則回退到 CPU


    # 載入訓練好的模型

    # 取得當前 Python 腳本的絕對路徑
    script_dir = Path(__file__).resolve().parent

    # 設定 YOLO 模型的正確路徑
    model_path = script_dir / "core/capoo/capoo_dogdog_training/weights/best.pt"

    # 載入模型
    model = YOLO(str(model_path))

    # 轉移到裝置（GPU 或 CPU）
    device = "cuda" if torch.cuda.is_available() else "cpu"
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
