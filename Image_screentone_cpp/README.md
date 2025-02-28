Image_screentone_cpp
-
It is the image processs for screenstone - C++ version

| Program | Type | Description | Input format |
|-------|-------|-------|-------|
| [Image_screentone](https://github.com/JIK-JHONG/side_project/blob/main/Image_screentone_cpp/Image_screentone.cpp) | C++ / OpenCV |Image processing | jpeg/png/... |
| [Image_screentone](https://github.com/JIK-JHONG/side_project/blob/main/Image_screentone_cpp/Image_screentone_mv.cpp) | C++ / OpenCV |Image processing | mp4...video|

ImageComicMesh_Mix(Mat image_input, int screentone_size, int screentone_gap, string screentone_type,string color_type) ;  
| Parameter | type | Description |
|-------|-------|-------|
| image_input | Mat | image input |
| screentone_size | int | size of screentone  |
| screentone_gap | int | gap between screentone |
| screentone_type | string | square || normal - shape of the screentone|
| color_type | string | std || grad - color of the screentone, std = depended on the color of the image , grad = default purple to pink|


| Original | Modified |
|-------|-------|
| ![Original](https://github.com/JIK-JHONG/side_project/blob/main/Image_screentone_cpp/sky_tree_tokyo.jpeg) | ![Original](https://github.com/JIK-JHONG/side_project/blob/main/Image_screentone_cpp/image_compare_set.jpeg) |

1. Left : Original
2. Middle :   ImageComicMesh_Mix(image_input, **1, 1, square, std**) 
3. Right :    ImageComicMesh_Mix(image_input, **1, 1, normal, grad**)
