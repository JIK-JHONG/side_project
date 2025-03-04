#include "image_process.h"
#include <iostream>
#include <cmath>

Mat ImageBlur(const Mat &input, Point start, Size area, Size blur_size)
{
    Mat output = input.clone();
    if (area.width == 0 || area.height == 0)
    {
        blur(output, output, blur_size);
    }
    else
    {
        Rect roi(start, area);
        Mat blurred_roi;
        blur(output(roi), blurred_roi, blur_size);
        blurred_roi.copyTo(output(roi));
    }
    return output;
}

int image_binary_color_check(const Mat &input, int threshold)
{
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    int white = 0;
    int black = 0;
    Mat tmp;
    if (channel == 3)
    {
        cvtColor(input, tmp, COLOR_BGR2GRAY);
    }
    else if (channel == 4)
    {
        cvtColor(input, tmp, COLOR_BGRA2GRAY);
    }
    else
    {
        tmp = input.clone();
    }
    for (int j = 0; j < height; j++)
    {
        for (int i = 0; i < width; i++)
        {
            if (tmp.at<Vec3b>(j, i)[0] > threshold)
            {
                white += 1;
            }
            else
            {
                black += 1;
            }
        }
    }
    printf("Auto_Check Ratio >> W = %.2f %% , B = %.2f %%\n", float(white)/(white+black)*100., float(black)/(white+black)*100.);
    if (white > black)
    {
        return 1;
    }
    else
    {
        return 0;
    }
}


Mat ImageGray(const Mat &input, int option)
{
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    Mat gray(height, width, CV_8UC3, Scalar(255, 255, 255));
    int max_color = 1;
    int min_color = 255;
    for (int j = 0; j < height; j++)
    {
        for (int i = 0; i < width; i++)
        {
            int tmp_balance = round(input.at<Vec3b>(j, i)[0] * 0.299 + input.at<Vec3b>(j, i)[1] * 0.587 + input.at<Vec3b>(j, i)[2] * 0.114);
            if (tmp_balance < min_color)
            {
                min_color = tmp_balance;
            }
            if (tmp_balance > max_color)
            {
                max_color = tmp_balance;
            }
        }
    }
    double factor_max = 255. / max_color;
    for (int j = 0; j < height; j++)
    {
        for (int i = 0; i < width; i++)
        {
            int tmp_balance = round(input.at<Vec3b>(j, i)[0] * 0.299 + input.at<Vec3b>(j, i)[1] * 0.587 + input.at<Vec3b>(j, i)[2] * 0.114);
            for (int k = 0; k < channel; k++)
            {
                int tmp = round(tmp_balance * factor_max);
                if (tmp > 255)
                {
                    tmp = 255;
                }
                gray.at<Vec3b>(j, i)[k] = tmp;
            }
        }
    }
    return gray;
}

Mat ImageBinary(const Mat &input, const std::string &mode_type, int low_threshold_force)
{
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    Mat output(height, width, CV_8UC3, Scalar(255, 255, 255));

    int low_threshold = low_threshold_force;
    int high_threshold = 255;

    if (mode_type == "normal")
    {
        for (int j = 0; j < height; j++)
        {
            for (int i = 0; i < width; i++)
            {
                int tmp_balance = (input.at<Vec3b>(j, i)[0] + input.at<Vec3b>(j, i)[1] + input.at<Vec3b>(j, i)[2]) / 3;
                for (int k = 0; k < channel; k++)
                {
                    if (tmp_balance > low_threshold)
                    {
                        tmp_balance = 255;
                    }
                    else
                    {
                        tmp_balance = 0;
                    }
                    output.at<Vec3b>(j, i)[k] = tmp_balance;
                }
            }
        }
    }
    else if (mode_type == "inverted")
    {
        for (int j = 0; j < height; j++)
        {
            for (int i = 0; i < width; i++)
            {
                int tmp_balance = (input.at<Vec3b>(j, i)[0] + input.at<Vec3b>(j, i)[1] + input.at<Vec3b>(j, i)[2]) / 3;
                for (int k = 0; k < channel; k++)
                {
                    int tmp = tmp_balance;
                    if (tmp_balance > low_threshold)
                    {
                        tmp = 0;
                    }
                    else
                    {
                        tmp = 255;
                    }
                    output.at<Vec3b>(j, i)[k] = tmp;
                }
            }
        }
    }
    else if (mode_type == "enhance")
    {
        for (int j = 0; j < height; j++)
        {
            for (int i = 0; i < width; i++)
            {
                int tmp_balance = (input.at<Vec3b>(j, i)[0] + input.at<Vec3b>(j, i)[1] + input.at<Vec3b>(j, i)[2]) / 3;
                for (int k = 0; k < channel; k++)
                {
                    int tmp = tmp_balance;
                    if (tmp_balance >= 0 && tmp_balance < 85)
                    {
                        tmp = 0;
                    }
                    else if (tmp_balance >= 85 && tmp_balance < 170)
                    {
                        tmp = 170;
                    }
                    else
                    {
                        tmp = 255;
                    }
                    output.at<Vec3b>(j, i)[k] = tmp;
                }
            }
        }
    }

    return output;
}


Mat ImageComicMesh_Mix(const Mat &input, int block_size, int gap_size, const std::string &option, std::string color_option)
{
    Mat input2;
    input2 = input.clone();
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    printf("Image = %d * %d (%d)\n", width, height, channel);
    int threshold = 5;
    Mat output(height, width, CV_8UC3, Scalar(255, 255, 255));
    int basic_color = 0;
    Vec3b color_mark(0, 0, 255);
    int fac = -1;
    Point initial_spot(round((block_size + gap_size)), round((block_size + gap_size)));
    printf("Scan_range = %d * %d (block_size = %d , gap_size = %d), mesh_size = %d \n", height / ((block_size + gap_size) * 2), width / ((block_size + gap_size) * 2), block_size, gap_size, (block_size + gap_size) * 2);

    int block_mesh_size = (block_size + gap_size) * 2 * (block_size + gap_size) * 2;
    int total_mesh_unit = 255 / (height / ((block_size + gap_size) * 2) * width / ((block_size + gap_size) * 2) / block_mesh_size);
    if (total_mesh_unit == 0)
    {
        total_mesh_unit = 1;
    }
    printf("block_mesh_size = %d\n", block_mesh_size);
    for (int j = 0; j < height / ((block_size + gap_size) * 2); j++)
    {
        for (int i = 0; i < width / ((block_size + gap_size) * 2); i++)
        {
            int sum_of_area = 0;
            int sum_color_b = 0;
            int sum_color_g = 0;
            int sum_color_r = 0;

            for (int kj = 0; kj < (block_size + gap_size) * 2; kj++)
            {
                for (int ki = 0; ki < (block_size + gap_size) * 2; ki++)
                {
                    int target_x = initial_spot.x + i * (block_size + gap_size) * 2 + ki - (block_size + gap_size);
                    int target_y = initial_spot.y + j * (block_size + gap_size) * 2 + kj - (block_size + gap_size);
                    if (target_x < width && target_y < height)
                    {
                        sum_of_area += (input2.at<Vec3b>(target_y, target_x)[0] + input2.at<Vec3b>(target_y, target_x)[1] + input2.at<Vec3b>(target_y, target_x)[2]) / 3;
                        sum_color_b += (input2.at<Vec3b>(target_y, target_x)[0]);
                        sum_color_g += (input2.at<Vec3b>(target_y, target_x)[1]);
                        sum_color_r += (input2.at<Vec3b>(target_y, target_x)[2]);
                    }
                }
            }
            sum_of_area /= block_mesh_size;
            sum_color_b /= block_mesh_size;
            sum_color_g /= block_mesh_size;
            sum_color_r /= block_mesh_size;
            if (sum_of_area <= 200)
            {
                Point center(initial_spot.x + i * (block_size + gap_size) * 2,
                             initial_spot.y + j * (block_size + gap_size) * 2);
                if (option == "normal")
                {
                    if (color_option == "std")
                    {
                        circle(output, center, block_size, Scalar(sum_color_b, sum_color_g, sum_color_r), fac);
                    }
                    else
                    {
                        circle(output, center, block_size, Scalar(255, 0, 0 + (i + j) * (total_mesh_unit)), fac);
                    }
                }
                else if (option == "square")
                {
                    if (color_option == "std")
                    {
                        rectangle(output,
                                  Point(center.x - block_size, center.y - block_size),
                                  Point(center.x + block_size, center.y + block_size),
                                  Scalar(sum_color_b, sum_color_g, sum_color_r),
                                  FILLED); // `FILLED` 代表填滿
                    }
                    else
                    {
                        rectangle(output,
                                  Point(center.x - block_size, center.y - block_size),
                                  Point(center.x + block_size, center.y + block_size),
                                  Scalar(255, 0, 0 + (i + j) * total_mesh_unit),
                                  FILLED); // `FILLED` 代表填滿
                    }
                }
            }
        }
    }

    return output;
}

int Calculate_White_Object(const Mat &input){
    int height = input.rows;
    int width = input.cols;
    int black_set = 0 ;
    for (int j=0;j<height;j++){
        for (int i=0;i<width;i++){
            int check_val = input.at<Vec3b>(j,i)[0];
            if (check_val == 0){
                black_set++;
            }
        }
    }
    return black_set;

}
Mat GRAY_2_RGB(const Mat &input){
    int channel = input.channels();
    int height = input.rows;
    int width = input.cols;
    Mat outout(height,width,CV_8UC3,Scalar(0, 0, 0));

    if (channel == 1){
        for (int j=0;j<height;j++){
            for (int i=0;i<width;i++){
                outout.at<Vec3b>(j,i)[0] = input.at<Vec3b>(j,i)[0];
                outout.at<Vec3b>(j,i)[1] = input.at<Vec3b>(j,i)[0];
                outout.at<Vec3b>(j,i)[2] = input.at<Vec3b>(j,i)[0];
            }
        }
    }else if (channel == 4){
        for (int j=0;j<height;j++){
            for (int i=0;i<width;i++){
                outout.at<Vec3b>(j,i)[0] = input.at<Vec3b>(j,i)[0];
                outout.at<Vec3b>(j,i)[1] = input.at<Vec3b>(j,i)[2];
                outout.at<Vec3b>(j,i)[2] = input.at<Vec3b>(j,i)[3];
            }
        }
    }else{
        outout = input.clone();
    }
    return outout;

}

Mat Rip_Object(const Mat &input,const Mat &Mask,int blur_size,int bks_blur_size){
    if (blur_size == 0){
        blur_size = 20;
    }
    int height = input.rows;
    int width = input.cols;
    Mat output(height,width, CV_8UC3, Scalar(0, 0, 0));
    for (int j=0;j<height;j++){
        for (int i=0;i<width;i++){
            output.at<Vec3b>(j,i)[0] = input.at<Vec3b>(j,i)[0];
            output.at<Vec3b>(j,i)[1] = input.at<Vec3b>(j,i)[1];
            output.at<Vec3b>(j,i)[2] = input.at<Vec3b>(j,i)[2];
        }
    }
    Mat buff = output.clone();
    // output = ImageBlur(input,Point(0, 0),Size(),Size(blur_size, blur_size));
    if (bks_blur_size > 0){
        if (bks_blur_size % 2 == 0){
            bks_blur_size++;
        }
        output = ImageBlur(input,Point(0, 0),Size(),Size(bks_blur_size, bks_blur_size));
    }
    for (int j=0;j<height;j++){
        for (int i=0;i<width;i++){
            int check_val = Mask.at<Vec3b>(j,i)[0];
            if (check_val > 0){
                output.at<Vec3b>(j,i)[0] = buff.at<Vec3b>(j,i)[0];
                output.at<Vec3b>(j,i)[1] = buff.at<Vec3b>(j,i)[1];
                output.at<Vec3b>(j,i)[2] = buff.at<Vec3b>(j,i)[2];
            }
        }
    }
    return output;
}
Mat Image_Test_Canny(const Mat &input,const Mat &original_img,const int paramter,const int paramter2,const int paramter3,const int paramter4,int option,int revise_select,int show_process,int bks_blur_size){
    Mat output = input.clone();
    int blur_size = paramter3;
    if (blur_size > 0){
        if (blur_size % 2 == 0){
            blur_size++;
        }
        output = ImageBlur(input,Point(0, 0),Size(),Size(blur_size, blur_size));
    }




    Mat buff = output.clone();
    Mat tmp = output.clone();
    Mat kernel = getStructuringElement(MORPH_RECT, Size(paramter4, paramter4));

    tmp = output.clone();
    if (option == 1){
        morphologyEx(tmp, output, MORPH_CLOSE, kernel);
        // tmp = output.clone();
        // morphologyEx(tmp, output, MORPH_OPEN, kernel);
    }else{
        morphologyEx(tmp, output, MORPH_OPEN, kernel);
        // tmp = output.clone();
        // morphologyEx(tmp, output, MORPH_CLOSE, kernel);
    }
    tmp = output.clone();
    if (paramter > 0){
        if (revise_select == 1){
            output = ImageBinary(tmp, "inverted", paramter);
        }else{
           output = ImageBinary(tmp, "normal", paramter);
        }
    }



    tmp = output.clone();
    // buff = output.clone();
    int blur_size_for_mask = paramter2;
    if (blur_size_for_mask > 0){
        if (blur_size_for_mask % 2 == 0){
            blur_size_for_mask++;
        }
        buff = ImageBlur(tmp,Point(0, 0),Size(),Size(blur_size_for_mask, blur_size_for_mask));
    }



    // Canny(tmp, output, paramter2, paramter2*2);
    // tmp = output.clone();


    // // // 尋找輪廓，只保留外輪廓
    // std::vector<std::vector<Point>> contours;
    // findContours(tmp, contours, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE);
    // // findContours(tmp, contours, RETR_TREE, CHAIN_APPROX_SIMPLE);

    // // // 創建一個新的影像來繪製輪廓
    Mat contourImg = Mat::zeros(output.size(), CV_8UC3);

    contourImg = tmp.clone();
    // // // 繪製外輪廓
    // // drawContours(contourImg, contours, -1, Scalar(0, 255, 0), 2);
    // for (size_t i = 1; i < contours.size(); i++) {
    //     // drawContours(contourImg, contours, i, Scalar(255), FILLED);
    //     drawContours(contourImg, contours, i, Scalar(0, 0, 255), FILLED);
    // }
    double total_area = static_cast<double>(input.cols) * static_cast<double>(input.rows);
    double area = 0 ;
    // // 計算並輸出每個輪廓的面積
    // for (size_t i = 1; i < contours.size(); i++) {
    //     area += contourArea(contours[i]); // 計算輪廓面積
    // }
    // // std::string msg = std::to_string(area) +" / " +std::to_string(total_area) + "( " + std::to_string(static_cast<int>(area / total_area * 100 )) + " % )" ;


    // contourImg = Rip_Object(input,buff,blur_size,bks_blur_size);


    if (show_process == 1){
        contourImg = buff.clone();
    }else{
        contourImg = Rip_Object(original_img,buff,blur_size,bks_blur_size);

    }
    // std::string msg = std::to_string(static_cast<int>(area / total_area * 100 )) + " %" ;
    std::string msg = std::to_string(Calculate_White_Object(buff) / total_area * 100) + "" ;


    putText(contourImg, msg, Point(50, 100), FONT_HERSHEY_SIMPLEX, 2.0, Scalar(0, 255, 0), 4);
    // msg = std::to_string(static_cast<int>(area)) + "" ;
    msg = std::to_string(Calculate_White_Object(buff)) + "" ;


    putText(contourImg, msg, Point(50, 200), FONT_HERSHEY_SIMPLEX, 2.0, Scalar(0, 255, 0), 4);
    msg = std::to_string(static_cast<int>(total_area)) + "" ;
    putText(contourImg, msg, Point(50, 300), FONT_HERSHEY_SIMPLEX, 2.0, Scalar(0, 255, 0), 4);
    return contourImg;
}
