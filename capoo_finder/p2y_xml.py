import os
import xml.etree.ElementTree as ET

# 定義類別（對應 classes.txt）
classes = ["Capoo", "Dogdog"]

# 輸入與輸出路徑
xml_folder = "test/labels/"
output_folder = "test/labels/"

os.makedirs(output_folder, exist_ok=True)

index =  0 
# 解析 XML 並轉換
for xml_file in os.listdir(xml_folder):
    if not xml_file.endswith(".xml"):
        continue

    tree = ET.parse(os.path.join(xml_folder, xml_file))
    root = tree.getroot()

    # 取得圖片尺寸
    size = root.find("size")
    width = int(size.find("width").text)
    height = int(size.find("height").text)

    # 建立 YOLO 標籤文件
    label_file = os.path.join(output_folder, xml_file.replace(".xml", ".txt"))
    with open(label_file, "w") as f:
        for obj in root.findall("object"):
            class_name = obj.find("name").text
            if class_name not in classes:
                print(f"跳過未知類別: {class_name}")
                continue

            class_id = classes.index(class_name)

            # 取得邊界框座標
            bndbox = obj.find("bndbox")
            xmin = int(bndbox.find("xmin").text)
            ymin = int(bndbox.find("ymin").text)
            xmax = int(bndbox.find("xmax").text)
            ymax = int(bndbox.find("ymax").text)

            # 計算 YOLO 格式數據
            x_center = (xmin + xmax) / 2 / width
            y_center = (ymin + ymax) / 2 / height
            bbox_width = (xmax - xmin) / width
            bbox_height = (ymax - ymin) / height

            # 寫入標籤文件
            f.write(f"{class_id} {x_center:.6f} {y_center:.6f} {bbox_width:.6f} {bbox_height:.6f}\n")
    
    print(f"[{index}]轉換完成！")
    index += 1 
print("轉換完成！")