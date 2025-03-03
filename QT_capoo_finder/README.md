QT_capoo_finder
-
It is the image processs for object detecting with GUI (QT creator)

It is using the training model for Capoo, Dogdog by YOLO.

# V1.1
Update the function of supporting CUDA / MPS for turning ON/OFF.

**I DON'T KNOW WHY MPS ON is SLOWER than CPU. :(**

ON
-
![Review](https://github.com/JIK-JHONG/side_project/blob/main/QT_capoo_finder/demo_mps.jpeg) 

OFF
-
![Review](https://github.com/JIK-JHONG/side_project/blob/main/QT_capoo_finder/demo_mps_dis.jpeg) 


**NOTE**

If you are using Apple Silicon CPU series (M1,M2,...last), is will use MPS to accelete the process for ML.



| Program | Type | Description |
|-------|-------|-------|
| [QT_capoo_finder](https://github.com/JIK-JHONG/side_project/blob/main/QT_capoo_finder) | python / OpenCV + QT | Object detecting |


![Review](https://github.com/JIK-JHONG/side_project/blob/main/QT_capoo_finder/demo.jpeg) 



# Memo
The image of YOLO is RGB and openCV is BRG, when send the image data to different function, need to be careful for the format.
