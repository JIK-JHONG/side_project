import os

FILE_DIR = "/Volumes/RamDisk/capoo2/"
FILE_NAME = "yolo11n_capoo_V2.yaml"
CONTENT_SET = ['capoo', 'dogdog']


ITEM_SET = ["train","val","test"]


with open(FILE_NAME, 'w') as f:
    for i in range(len(ITEM_SET)):
        f.write(f"{ITEM_SET[i]}: {FILE_DIR}{ITEM_SET[i]}/images")
        f.write("\n")
    f.write(f"# Classes")
    f.write("\n")
    f.write(f"nc: {len(CONTENT_SET)}")
    f.write("\n")
    
    names_set = ""
    for j in range(len(CONTENT_SET)):
        if j < len(CONTENT_SET) - 1 :
            names_set += f"'{CONTENT_SET[j]}' , " 
        else:
            names_set += f"'{CONTENT_SET[j]}'" 
    
    f.write(f"names: [{names_set}]")
