"""
檔案名稱: Image_analysis.py
語言版本: Python 3.12
編譯器/執行環境: MacOS

描述:
影像強度分析。

作者: JIK JHONG
日期: 2025.02.27
更新日期: 2025.02.27

版本: v1.0

參考文獻或相關連結:

"""


import cv2
import numpy as np
import matplotlib.pyplot as plt
import os

input_image = "birds_img.jpeg"
option = "mix"

def image_info(input_image):
    image = cv2.imread(input_image, cv2.IMREAD_UNCHANGED)
    
    if image is None:
        print("Error: Could not open image!")
        return
    
    height, width, channels = image.shape if len(image.shape) == 3 else (image.shape[0], image.shape[1], 1)
    
    image_type = "Unknown"
    if channels == 1:
        image_type = "GRAY"  # Single channel
    elif channels == 3:
        image_type = "BGR"   # OpenCV default BGR
    elif channels == 4:
        image_type = "BGRA"  # Including alpha channel
    
    print(f"---\nInfo: Image W x H ({image_type}) = ({width} x {height})\n---")
    return image

def save_image(image, output_filename):
    if not cv2.imwrite(output_filename, image):
        print(f"Error: Could not save image to {output_filename}")

def image_pick_color(input_image, option="red", force_use=0, low_threshold_set=60):
    image = cv2.imread(input_image)
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

def image_analysis(input_image, option="all"):
    image = cv2.imread(input_image)
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

        # with open("color_intensity_map.txt", "w") as file:
        #     for i in range(256):
        #         file.write(f"{i} {intensity[i]}\n")

        # Plotting with matplotlib
        plt.figure()
        plt.bar(range(256), intensity, color='blue')
        plt.xlim([0,255])
        plt.title("Gray Intensity Distribution")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.savefig('output_py.png')

    elif option == "div":
        image_intensity_r = image_pick_color(input_image, "red")
        image_intensity_g = image_pick_color(input_image, "green")
        image_intensity_b = image_pick_color(input_image, "blue")
        
        intensity_r = np.zeros(256, dtype=int)
        intensity_g = np.zeros(256, dtype=int)
        intensity_b = np.zeros(256, dtype=int)
        
        for j in range(image.shape[0]):
            for i in range(image.shape[1]):
                intensity_r[image_intensity_r[j, i, 2]] += 1
                intensity_g[image_intensity_g[j, i, 1]] += 1
                intensity_b[image_intensity_b[j, i, 0]] += 1

        # with open("color_intensity_rgb_map.txt", "w") as file:
        #     for i in range(256):
        #         file.write(f"{i} {intensity_r[i]} {intensity_g[i]} {intensity_b[i]}\n")

        # Plotting RGB intensity with matplotlib
        plt.figure()
        plt.bar(range(256), intensity_r, color='red', alpha=0.5, label='Red')
        plt.bar(range(256), intensity_g, color='green', alpha=0.5, label='Green')
        plt.bar(range(256), intensity_b, color='blue', alpha=0.5, label='Blue')
        plt.xlim([0,255])
        plt.title("RGB Intensity Distribution")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.legend()
        plt.savefig('output_rgb_py.png')

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

        # with open("color_intensity_map.txt", "w") as file:
        #     for i in range(256):
        #         file.write(f"{i} {intensity[i]}\n")
        image_intensity_r = image_pick_color(input_image, "red")
        image_intensity_g = image_pick_color(input_image, "green")
        image_intensity_b = image_pick_color(input_image, "blue")
        
        intensity_r = np.zeros(256, dtype=int)
        intensity_g = np.zeros(256, dtype=int)
        intensity_b = np.zeros(256, dtype=int)
        
        for j in range(image.shape[0]):
            for i in range(image.shape[1]):
                intensity_r[image_intensity_r[j, i, 2]] += 1
                intensity_g[image_intensity_g[j, i, 1]] += 1
                intensity_b[image_intensity_b[j, i, 0]] += 1

        # with open("color_intensity_rgb_map.txt", "w") as file:
        #     for i in range(256):
        #         file.write(f"{i} {intensity_r[i]} {intensity_g[i]} {intensity_b[i]}\n")

        # Plotting RGB intensity with matplotlib
        plt.figure()
        plt.fill_between(range(256), intensity, color='gray', alpha=0.8, label='Intensity')
        plt.bar(range(256), intensity_r, color='red', alpha=0.5, label='Red')
        plt.bar(range(256), intensity_g, color='green', alpha=0.5, label='Green')
        plt.bar(range(256), intensity_b, color='blue', alpha=0.5, label='Blue')
        plt.xlim([0,255])
        plt.title("RGB + Intensity Distribution")
        plt.xlabel("Pixel Value")
        plt.ylabel("Frequency")
        plt.legend()
        plt.savefig('output_rgb_mix_py.png')
        


def main():
    image = image_info(input_image)
    if image is not None:
        # image_analysis(input_image, "all")
        # image_analysis(input_image, "div")
        image_analysis(input_image, option)

if __name__ == "__main__":
    main()