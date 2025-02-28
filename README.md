Image Process, Automated Assistant Programs
-
python      : v3.12

c++(g++)    : v11

MacOS       : v14 ~ latest


| Header_Name | Description | Description | 
|-------|-------|-------|
| Image_ | Image Processing| C++ / Python / openCV ... |
| pgui_ | Programs with GUI |Python + tkinter |


**Image Process**

| Program | Type | Description |
|-------|-------|-------|
| [Image_color_offset](https://github.com/JIK-JHONG/side_project/tree/main/Image_color_offset) | OpenCV | Image Processing - Color Offset (python)|
| [Image_object_detected](https://github.com/JIK-JHONG/side_project/tree/main/Image_object_detected) | OpenCV | Object Detection (C++)|
| [Image_screentone_cpp](https://github.com/JIK-JHONG/side_project/tree/main/Image_screentone_cpp) | OpenCV | Image Processing - screentone (C++) |
| [Image_Intensity_analysis](https://github.com/JIK-JHONG/side_project/tree/main/Image_Intensity_analysis) | OpenCV | Image Processing - Analysis Intensity (C++/Python) |
| [capoo_finder](https://github.com/JIK-JHONG/side_project/tree/main/capoo_finder) | OpenCV+YOLO | specified Object Detection (including model - for [Capoo](https://zh.wikipedia.org/zh-tw/貓貓蟲咖波)) - which training by myself with photos which I token.

Note: **[capoo_finder](https://github.com/JIK-JHONG/side_project/tree/main/capoo_finder)** using for identify **capoo** and **dogdog** only.

**Assistant Programs**

| Program | Type | Description |
|-------|-------|-------|
| [thermal_conductivity](https://github.com/JIK-JHONG/side_project/tree/main/thermal_conductivity) | python+flask+PyTorch | predict thermal conductivity for input temperature and power (fake model) |
| [pgui_4ch_plot](https://github.com/JIK-JHONG/side_project/tree/main/pgui_4ch_plot) | python+tkinter | Automated analysis the experiment files(*.4ch) |
| [pgui_step_function](https://github.com/JIK-JHONG/side_project/tree/main/pgui_step_function.py) | python+tkinter | Generated the diagram of step function for report. |
| [pgui_worm](https://github.com/JIK-JHONG/side_project/tree/main/pgui_worm.py) | python+tkinter+BeautifulSoup | web crawler for ptt |

Note: You **NEED** install the relative package for those applications
Python
1. pip install tk
2. pip install bs4
3. pip install opencv-python
C++
4. brew install opencv

