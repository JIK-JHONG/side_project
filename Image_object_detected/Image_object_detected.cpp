/**********************************************************************
 * 檔案名稱: Image_object_detected.cpp
 * 語言版本: C++
 * 編譯器: g++ 11
 * 
 * 描述:
 * 影像處理，物件偵測，與統計
 * 
 * 作者: JIK JHONG
 * 日期: 2025.02.27
 * 更新日期: 2025.02.27
 * 
 * 版本: v1.0
 * 
 * 參考文獻或相關連結:
 * N.A.
 *********************************************************************/
#include <opencv2/opencv.hpp>
#include <iostream>
#include <filesystem>
#include <fstream>


using namespace cv;
using namespace std;

int save_div_image = 0 ;    // 儲存個別已辨識檔案，作為訓練用途。（ 0 = false , 1 = true）

// Point2f 相關應用：
// 定義點：         Point2f pt(10.5, 20.5); 
// 計算距離：       float dist = norm(pt1 - pt2);
// 用於影像變換：    Mat rotMat = getRotationMatrix2D(Point2f(100, 100), 30, 1.0);


// CV_8UC1	8-bit 單通道（灰階影像）
// CV_8UC3	8-bit 三通道（BGR 彩色影像）
// CV_8UC4	8-bit 四通道（BGRA，含透明度）
// CV_16UC1	16-bit 無符號整數灰階影像
// CV_16SC1	16-bit 有符號整數灰階影像
// CV_32FC1	32-bit 浮點數灰階影像
// CV_64FC1	64-bit 浮點數灰階影像


array<int, 3> image_info(const Mat &input){
    if (input.empty()) {
        cerr << "Error: Could not open image!" << endl;
        return {0, 0, 0};
    }
    array<int, 3> dim;
    dim[0] = input.rows;
    dim[1] = input.cols;
    dim[2] = input.channels();
    return dim;
}

void image_info_c(const Mat &input, int *dim){
    if (input.empty()) {
        cerr << "Error: Could not open image!" << endl;
        return ;
    }
    dim[0] = input.rows;
    dim[1] = input.cols;
    dim[2] = input.channels();
    string image_type;
    if (dim[2] == 1) {
        image_type = "GRAY";  // 單通道
    } else if (dim[2] == 3) {
        image_type = "BGR";   // OpenCV 預設 BGR
    } else if (dim[2] == 4) {
        image_type = "BGRA";  // 含透明通道
    } else {
        image_type = "Unknown";
    }

    // printf("Info Image W = %d , H = %d , C = %d\n",dim[0],dim[1],dim[2]);
    printf("---\n");
    printf("Info: Image W x H ( %s ) = ( %d x %d )\n", image_type.c_str(), dim[1], dim[0]);
    printf("---\n");
    
}


Mat load_image(const string &filepath){
    Mat image_read = imread(filepath, IMREAD_UNCHANGED);
    if (image_read.empty()) {
        cerr << "Error: Unable to open image " << filepath << endl;
    }
    return image_read;
}

void saveImage(const Mat &image, const string &outputFilename) {
    if (!imwrite(outputFilename, image)) {
        cerr << "Error: Could not save image to " << outputFilename << endl;
    }
}


Mat Image_Add_Layer_3c(const Mat &input,const Mat &input2,const Mat &input3, int fac=1, int fac2=1, int fac3=1){
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    Mat output(height,width, CV_8UC3, Scalar(0, 0, 0));

    for (int j=0;j<height;j++){
        for (int i=0;i<width;i++){
            for (int k=0;k<channel;k++){
                output.at<Vec3b>(j, i)[k] = int((input.at<Vec3b>(j, i)[k] * fac + input2.at<Vec3b>(j, i)[k] * fac2 + input3.at<Vec3b>(j, i)[k] * fac3)) ;   
            }     
        }
    }
    return output;

}


void image_preProcess(Mat &input){
    int channel = input.channels();
    if (channel == 1){
        cvtColor(input, input, COLOR_GRAY2BGR);
        printf("image_input > to RGB\n");
    }else{
        printf("image_input > unchanged\n");
    }

}

void Compare_View4(const Mat &input, const Mat &input2, const Mat &input3, const Mat &input4){
    int height = input.rows;
    int width = input.cols;

    // 轉換成 BGR 以便顯示
    Mat output_tmp, output_tmp2, output_tmp3, output_tmp4;
    output_tmp = input.clone();
    output_tmp2 = input2.clone();
    output_tmp3 = input3.clone();
    output_tmp4 = input4.clone();

    image_preProcess(output_tmp);
    image_preProcess(output_tmp2);
    image_preProcess(output_tmp3);
    image_preProcess(output_tmp4);

    // 建立寬度加倍的影像來放置三張影像
    int width_compare = width * 4;
    Mat output(height, width_compare, CV_8UC3, Scalar(255, 255, 255));
    // 複製影像到 output
    output_tmp.copyTo(output(Rect(0, 0, width, height)));         // 左邊
    output_tmp2.copyTo(output(Rect(width, 0, width, height)));    // 中間
    output_tmp3.copyTo(output(Rect(width * 2, 0, width, height))); // 右邊
    output_tmp4.copyTo(output(Rect(width * 3, 0, width, height))); // 右邊
    saveImage(output,"image_compare_set.jpeg");
    imshow("Output", output);
    waitKey(0);
}


void show_image_rgb(const Mat& input){
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    int total_mesh = height * width ; 
    double sum_r = 0 ;
    double sum_g = 0 ;
    double sum_b = 0 ;

    for (int j=0;j<height;j++){
        for (int i=0;i<width;i++){
            sum_b += double(input.at<Vec3b>(j, i)[0]) / 255.;
            sum_g += double(input.at<Vec3b>(j, i)[1]) / 255.;
            sum_r += double(input.at<Vec3b>(j, i)[2]) / 255.;
        }
    }

    printf("---\n");
    printf("Ave : R = %d , G = %d , B = %d\n", int(sum_r/total_mesh*255), int(sum_g/total_mesh*255), int(sum_b/total_mesh*255));
    printf("---\n");


}




void init_rgba2rgb(Mat& input){
    cvtColor(input, input, cv::COLOR_BGRA2BGR);
}

int main(){
    string file_name = "bird_insky.jpeg";    
    Mat image = load_image(file_name); 
    int *array_info = (int*) malloc(sizeof(int) * 3);
    if (array_info == nullptr) {
        cerr << "Memory allocation failed!" << endl;
        return -1;  // 退出程序
    }

    if (image.channels()==4){
        printf("為RGBA圖檔類型，進行轉換為RGB\n");
        init_rgba2rgb(image);
    }
    


    image_info_c(image, array_info);
    printf("Image W = %d , H = %d , C = %d\n",array_info[0],array_info[1],array_info[2]);

    Mat copy_set = image.clone();
    show_image_rgb(copy_set);


    Mat img_with_contours_b ;
    cvtColor(image,img_with_contours_b,COLOR_BGR2GRAY);
    int kernel_size = 4 ;
    cv::Mat kernel = cv::getStructuringElement(cv::MORPH_RECT, cv::Size(kernel_size, kernel_size)); // 5x5 矩形結構元素
    cv::morphologyEx(img_with_contours_b, img_with_contours_b, cv::MORPH_OPEN, kernel);
    threshold(img_with_contours_b,img_with_contours_b,90,255,THRESH_BINARY);

    std::vector<std::vector<Point>> contours;
    findContours(img_with_contours_b, contours, RETR_TREE, CHAIN_APPROX_NONE);
    Mat img_with_contours = image.clone();

    drawContours(img_with_contours, contours, -1, Scalar(0, 255, 0), 4); // 畫出綠色輪廓   

    // 建立遮罩影像
    Mat mask_image(image.size(), CV_8U, Scalar(0));

    // 繪製所有輪廓
    for (size_t i = 1; i < contours.size(); i++) {
        drawContours(mask_image, contours, i, Scalar(255), FILLED);
    }

    // 建立結果影像，只保留輪廓內的內容
    Mat result(image.size(),CV_8UC3, Scalar(255, 255, 255));
    image.copyTo(result, mask_image);


    for (size_t i = 1; i < contours.size(); i++) {
        int shift_mesh = 10 ;
        Rect rect = boundingRect(contours[i]);  // 找出輪廓的外接矩形
        if (save_div_image == 1){
            Mat cropped = image(rect);  // 從原圖裁剪出該區域
            imwrite("cropped_contour_" + to_string(i) + ".jpeg", cropped);
        }
        string text = to_string(i);
        Point textPos(rect.x , rect.y - shift_mesh);  // 文字的位置
        int font = FONT_HERSHEY_SIMPLEX;
        double fontScale = 0.8;
        Scalar textColor(255, 0, 0);  // 文字顏色 (白色)
        int thickness = 2;
        putText(result, text, textPos, font, fontScale, textColor, thickness);
    }
    printf("Total_Object =  %zu  detected\n",(contours.size()));
    Compare_View4(image, img_with_contours, mask_image, result);
    

}
