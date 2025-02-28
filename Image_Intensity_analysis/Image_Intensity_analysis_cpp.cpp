/**********************************************************************
 * 檔案名稱: Image_Intensity_analysis_cpp.cpp
 * 語言版本: C++
 * 編譯器: g++ 11
 *
 * 描述:
 * 影片處理，網點特效
 *
 * 作者: JIK JHONG
 * 日期: 2025.02.27
 * 更新日期: 2025.02.27
 *
 * 版本: v1.0
 * 1.0 影像強度分析。
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
string input_image = "cat_img.jpeg";
string option = "mix";


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


Mat Image_Pick_Color(const Mat &input, string option="red",int force_use = 0 ,int low_threshold_set = 60){
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    int channel_set = 2 ;
    int low_threshold = low_threshold_set;
    Mat output(height,width, CV_8UC3, Scalar(0, 0, 0));

    if (option == "red"){
        channel_set = 2; 
    }else if (option == "green"){
        channel_set = 1; 
    }else if (option == "blue"){
        channel_set = 0; 
    }
    for (int j=0;j<height;j++){
        for (int i=0;i<width;i++){
            if (force_use == 1){
                if (input.at<Vec3b>(j, i)[channel_set] > low_threshold){
                    output.at<Vec3b>(j, i)[channel_set] = 255;              
                }else{
                    output.at<Vec3b>(j, i)[channel_set] = input.at<Vec3b>(j, i)[channel_set];               
                }
            }else{
                output.at<Vec3b>(j, i)[channel_set] = input.at<Vec3b>(j, i)[channel_set];      
            }
            
        }
    }
    return output;
}


void image_analysis(const Mat &input, string option="all") {
    Mat tmp;
    int channel = input.channels();
    if (option=="all"){
        // 如果不是灰階圖，則轉換為灰階圖
        if (channel != 1) {
            if (channel == 3) {
                cvtColor(input, tmp, cv::COLOR_BGR2GRAY);
            } else if (channel == 4) {
                cvtColor(input, tmp, cv::COLOR_BGRA2GRAY);
            }
        } else {
            tmp = input; // 如果已經是灰階圖，直接使用輸入影像
        }
        vector<int> intensity(256, 0);

        // 遍歷影像的每一個像素
        for (int j = 0; j < tmp.rows; j++) {
            for (int i = 0; i < tmp.cols; i++) {
                // 如果是灰階圖，取單一通道的像素值
                intensity[tmp.at<uchar>(j, i)]++; 
            }
        }

        // 顯示每個像素值的頻率
        for (int i = 0; i < 256; i++) {
            printf("[%d] = %d\n", i, intensity[i]);
        }
        // 輸出數據到檔案
        ofstream file("color_intensity_map.txt");

        for (size_t i = 0; i < intensity.size(); ++i) {
            file << i << " " << intensity[i] << endl;  // 寫入灰階強度和對應頻率
        }
        file.close();

        // 使用 Gnuplot 繪製直條圖
        system("gnuplot -e \"set terminal png; set output 'output.png'; set style fill solid; set boxwidth 0.5;set xrange [0:255]; plot 'color_intensity_map.txt' with boxes lc rgb 'blue'\"");
    }else if(option=="div"){
        Mat image_intensity_r, image_intensity_g, image_intensity_b;
        // 假設 Image_Pick_Color 函數會從影像中提取指定通道的像素
        image_intensity_r = Image_Pick_Color(input, "red");
        image_intensity_g = Image_Pick_Color(input, "green");
        image_intensity_b = Image_Pick_Color(input, "blue");
        
        vector<int> intensity_r(256, 0);
        vector<int> intensity_g(256, 0);
        vector<int> intensity_b(256, 0);
        
        // 遍歷影像的每一個像素並統計每個通道的頻率
        for (int j = 0; j < input.rows; j++) {
            for (int i = 0; i < input.cols; i++) {
                intensity_r[image_intensity_r.at<Vec3b>(j, i)[2]]++;  // 累計紅色通道強度
                intensity_g[image_intensity_g.at<Vec3b>(j, i)[1]]++;  // 累計綠色通道強度
                intensity_b[image_intensity_b.at<Vec3b>(j, i)[0]]++;  // 累計藍色通道強度
            }
        }
        intensity_r[0] = 0 ;
        intensity_b[0] = 0 ;
        intensity_g[0] = 0 ;
        // 輸出每個通道的數據到檔案
        ofstream file("color_intensity_rgb_map.txt");
        
        for (int i = 0; i < 256; ++i) {
            // 輸出紅色、綠色、藍色通道的強度頻率
            file << i << " " << intensity_r[i] << " " << intensity_g[i] << " " << intensity_b[i] << endl;
        }
        
        file.close();
        
        // 使用 Gnuplot 繪製三個通道的直條圖
        system("gnuplot -e \"set terminal png; set output 'output_rgb.png'; "
            "set style fill solid; set boxwidth 0.5; "
            "set xrange [0:255];"
            "plot 'color_intensity_rgb_map.txt' using 1:2 with boxes lc rgb 'red', "
            "'color_intensity_rgb_map.txt' using 1:3 with boxes lc rgb 'green', "
            "'color_intensity_rgb_map.txt' using 1:4 with boxes lc rgb 'blue'\"");
    }else{
        // 如果不是灰階圖，則轉換為灰階圖
        if (channel != 1) {
            if (channel == 3) {
                cvtColor(input, tmp, cv::COLOR_BGR2GRAY);
            } else if (channel == 4) {
                cvtColor(input, tmp, cv::COLOR_BGRA2GRAY);
            }
        } else {
            tmp = input; // 如果已經是灰階圖，直接使用輸入影像
        }

        // 初始化一個大小為 256 的 vector 來存放每個像素值的頻率
        vector<int> intensity(256, 0);

        // 遍歷影像的每一個像素
        for (int j = 0; j < tmp.rows; j++) {
            for (int i = 0; i < tmp.cols; i++) {
                intensity[tmp.at<uchar>(j, i)]++; 
            }
        }

        // 輸出灰階強度數據到檔案
        ofstream file("color_intensity_map.txt");
        for (size_t i = 0; i < intensity.size(); ++i) {
            file << i << " " << intensity[i] << endl;  // 寫入灰階強度和對應頻率
        }
        file.close();

        // 假設 Image_Pick_Color 函數會從影像中提取指定通道的像素
        Mat image_intensity_r = Image_Pick_Color(input, "red");
        Mat image_intensity_g = Image_Pick_Color(input, "green");
        Mat image_intensity_b = Image_Pick_Color(input, "blue");

        vector<int> intensity_r(256, 0);
        vector<int> intensity_g(256, 0);
        vector<int> intensity_b(256, 0);

        
        // 遍歷影像的每一個像素並統計每個通道的頻率
        for (int j = 0; j < input.rows; j++) {
            for (int i = 0; i < input.cols; i++) {
                intensity_r[image_intensity_r.at<Vec3b>(j, i)[2]]++;  // 累計紅色通道強度
                intensity_g[image_intensity_g.at<Vec3b>(j, i)[1]]++;  // 累計綠色通道強度
                intensity_b[image_intensity_b.at<Vec3b>(j, i)[0]]++;  // 累計藍色通道強度
            }
        }

        intensity_r[0] = 0;
        intensity_b[0] = 0;
        intensity_g[0] = 0;

        // 輸出每個通道的數據到檔案
        ofstream file_rgb("color_intensity_rgb_map.txt");

        for (int i = 0; i < 256; ++i) {
            // 輸出紅色、綠色、藍色通道的強度頻率
            file_rgb << i << " " << intensity_r[i] << " " << intensity_g[i] << " " << intensity_b[i] << endl;
        }

        file_rgb.close();

        // 使用 Gnuplot 繪製綜合圖：RGB直條圖+灰階強度的綜合線條圖（淡黃色半透明背景）
        system("gnuplot -e \"set terminal png; set output 'output_all_mix.png'; "
            "set style fill transparent solid 0.1; set boxwidth 0.5; "
            "set xrange [0:255];"
            // 畫灰階強度的填充曲線和線條
            "plot 'color_intensity_map.txt' using 1:2 with filledcurves title 'Gray Intensity' lc rgb 'gray', "
            // 依次畫出 RGB 直條圖
            "'color_intensity_rgb_map.txt' using 1:2 with boxes lc rgb 'red', "
            "'color_intensity_rgb_map.txt' using 1:3 with boxes lc rgb 'green', "
            "'color_intensity_rgb_map.txt' using 1:4 with boxes lc rgb 'blue'\"");
        cout << "Profile of Image - output_all_mix.png is saving." << endl;
    } 
}

void init_rgba2rgb(Mat& input){
    cvtColor(input, input, cv::COLOR_BGRA2BGR);
}

int main(){
    string file_name = input_image;    
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
    

    image_analysis(image,option);
    image_info_c(image, array_info);
    
    

}