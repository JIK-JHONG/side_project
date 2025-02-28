/**********************************************************************
 * 檔案名稱: Image_screentone.cpp
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
 * 版本: v1.1
 * 1.1 新增自我判斷整體黑白比例，作為是否要進行影像黑白反轉依據。
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

// CV_8UC1	8-bit 單通道（灰階影像）
// CV_8UC3	8-bit 三通道（BGR 彩色影像）
// CV_8UC4	8-bit 四通道（BGRA，含透明度）
// CV_16UC1	16-bit 無符號整數灰階影像
// CV_16SC1	16-bit 有符號整數灰階影像
// CV_32FC1	32-bit 浮點數灰階影像
// CV_64FC1	64-bit 浮點數灰階影像

array<int, 3> image_info(const Mat &input)
{
    if (input.empty())
    {
        cerr << "Error: Could not open image!" << endl;
        return {0, 0, 0};
    }
    array<int, 3> dim;
    dim[0] = input.rows;
    dim[1] = input.cols;
    dim[2] = input.channels();
    return dim;
}

void image_info_c(const Mat &input, int *dim)
{
    if (input.empty())
    {
        cerr << "Error: Could not open image!" << endl;
        return;
    }
    dim[0] = input.rows;
    dim[1] = input.cols;
    dim[2] = input.channels();
    string image_type;
    if (dim[2] == 1)
    {
        image_type = "GRAY"; // 單通道
    }
    else if (dim[2] == 3)
    {
        image_type = "BGR"; // OpenCV 預設 BGR
    }
    else if (dim[2] == 4)
    {
        image_type = "BGRA"; // 含透明通道
    }
    else
    {
        image_type = "Unknown";
    }

    printf("---\n");
    printf("Info: Image W x H ( %s ) = ( %d x %d )\n", image_type.c_str(), dim[1], dim[0]);
    printf("---\n");
}

Mat load_image(const string &filepath)
{
    Mat image_read = imread(filepath, IMREAD_UNCHANGED);
    if (image_read.empty())
    {
        cerr << "Error: Unable to open image " << filepath << endl;
    }
    return image_read;
}

void saveImage(const Mat &image, const string &outputFilename)
{
    if (!imwrite(outputFilename, image))
    {
        cerr << "Error: Could not save image to " << outputFilename << endl;
    }
}

Mat ImageBlur(const Mat &input, Point start = Point(0, 0), Size area = Size(), Size blur_size = Size(50, 50))
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

Mat ImageGray(const Mat &input, int option = 1)
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
    printf("Max_Fac = %f\n", factor_max);
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

Mat ImageBinary(const Mat &input, const std::string &mode_type = "normal", int low_threshold_force = 127)
{
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    printf("C = %d\n", channel);
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
        // int mid_threshold = (low_threshold + high_threshold) / 2 ;
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

Mat ImageComicMesh_Mix(const Mat &input, int block_size = 20, int gap_size = 2, const string &option = "normal", string color_option = "std")
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

Mat Pixelized(const Mat &input, int pixel_size = 10)
{
    int height = input.rows;
    int width = input.cols;
    int channel = input.channels();
    int height_pixel = height / pixel_size;
    int width_pixel = width / pixel_size;
    int pixel_area = pixel_size * pixel_size;

    Mat output(height, width, CV_8UC3, Scalar(0, 0, 0));

    for (int j = 0; j < height_pixel + 1; j++)
    {
        for (int i = 0; i < width_pixel + 1; i++)
        {
            int sub_r = 0;
            int sub_g = 0;
            int sub_b = 0;
            for (int kj = 0; kj < pixel_size; kj++)
            {
                for (int ki = 0; ki < pixel_size; ki++)
                {
                    sub_r += input.at<Vec3b>(j * pixel_size + kj, i * pixel_size + ki)[2];
                    sub_g += input.at<Vec3b>(j * pixel_size + kj, i * pixel_size + ki)[1];
                    sub_b += input.at<Vec3b>(j * pixel_size + kj, i * pixel_size + ki)[0];
                }
            }
            sub_r /= pixel_area;
            sub_g /= pixel_area;
            sub_b /= pixel_area;
            sub_r = int(sub_r);
            sub_g = int(sub_g);
            sub_b = int(sub_b);

            for (int kj = 0; kj < pixel_size; kj++)
            {
                for (int ki = 0; ki < pixel_size; ki++)
                {
                    output.at<Vec3b>(j * pixel_size + kj, i * pixel_size + ki)[2] = sub_r;
                    output.at<Vec3b>(j * pixel_size + kj, i * pixel_size + ki)[1] = sub_g;
                    output.at<Vec3b>(j * pixel_size + kj, i * pixel_size + ki)[0] = sub_b;
                }
            }
        }
    }
    return output;
}

void image_preProcess(Mat &input)
{
    int channel = input.channels();
    if (channel == 1)
    {
        cvtColor(input, input, COLOR_GRAY2BGR);
        printf("image_input > to RGB\n");
    }
    else
    {
        printf("image_input > unchanged\n");
    }
}
void Compare_View(const Mat &input, const Mat &input2, const Mat &input3)
{
    int height = input.rows;
    int width = input.cols;

    // 轉換成 BGR 以便顯示
    Mat output_tmp, output_tmp2, output_tmp3;
    output_tmp = input.clone();
    output_tmp2 = input2.clone();
    output_tmp3 = input3.clone();

    image_preProcess(output_tmp);
    image_preProcess(output_tmp2);
    image_preProcess(output_tmp3);

    // 建立寬度加倍的影像來放置三張影像
    int width_compare = width * 3;
    Mat output(height, width_compare, CV_8UC3, Scalar(255, 255, 255));
    // 複製影像到 output
    output_tmp.copyTo(output(Rect(0, 0, width, height)));          // 左邊
    output_tmp2.copyTo(output(Rect(width, 0, width, height)));     // 中間
    output_tmp3.copyTo(output(Rect(width * 2, 0, width, height))); // 右邊
    saveImage(output, "image_compare_set.jpeg");
    imshow("Output", output);
    waitKey(0);
}

int image_binary_color_check(const Mat &input, int threshold = 80)
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

void init_rgba2rgb(Mat &input)
{
    cvtColor(input, input, cv::COLOR_BGRA2BGR);
}

void video_info_c(const VideoCapture &cap){
    // 取得影片的基本資訊
    double width = cap.get(cv::CAP_PROP_FRAME_WIDTH);   // 影片寬度
    double height = cap.get(cv::CAP_PROP_FRAME_HEIGHT); // 影片高度
    double fps = cap.get(cv::CAP_PROP_FPS);            // 幀率 (frames per second)
    double totalFrames = cap.get(cv::CAP_PROP_FRAME_COUNT); // 總幀數
    int codec = static_cast<int>(cap.get(cv::CAP_PROP_FOURCC)); // 影片的編碼格式
    // 解碼編碼格式
    char codecStr[] = {
        static_cast<char>(codec & 0xFF),
        static_cast<char>((codec >> 8) & 0xFF),
        static_cast<char>((codec >> 16) & 0xFF),
        static_cast<char>((codec >> 24) & 0xFF),
        '\0'
    };
    printf("---\n");
    printf("影片資訊(W X H)： %d X %d @%.2f fps (%d frames)\n",int(width),int(height), fps, int(totalFrames));
    printf("影片格式： %s\n",codecStr);  
    printf("---\n");  

}

int main(){
    std::string videoPath = "IMG_0774.MOV";  // 影片檔案路徑
    std::string outputVideoPath = "output_video_screentone_cpp.mp4";
    cv::VideoCapture cap(videoPath, cv::CAP_FFMPEG);
    video_info_c(cap);
    if (!cap.isOpened()) {
        std::cerr << "無法開啟影片檔案！" << std::endl;
        return -1;
    }

    // 取得影片資訊
    double width = cap.get(cv::CAP_PROP_FRAME_WIDTH);
    double height = cap.get(cv::CAP_PROP_FRAME_HEIGHT);
    double fps = cap.get(cv::CAP_PROP_FPS);
    if (fps <= 0) {
        std::cerr << "警告：FPS 讀取失敗，預設為 30 FPS" << std::endl;
        fps = 30;  // 設定預設值
    }

    // 初始化 VideoWriter（確保 H.264 正確寫入）
    cv::VideoWriter writer(
        outputVideoPath,
        cv::VideoWriter::fourcc('a', 'v', 'c', '1'),  // H.264
        fps,
        cv::Size(static_cast<int>(width), static_cast<int>(height)),
        true // 必須為 true，H.264 需要 3 通道彩色影像
    );

    if (!writer.isOpened()) {
        std::cerr << "無法建立輸出影片檔案！請確認 FFmpeg 是否支援 H.264。" << std::endl;
        return -1;
    }

    // 創建視窗
    cv::namedWindow("Original Video", cv::WINDOW_AUTOSIZE);
    cv::namedWindow("Processed Video", cv::WINDOW_AUTOSIZE);

    cv::Mat frame, grayFrame, edgeFrame, edgeFrameColor;
    int idx = 0;
    int div_output = 0 ;
    while (true) {
        cap >> frame; // 讀取當前幀
        if (frame.empty()) break; // 如果讀取失敗，則跳出迴圈
        Mat copy_set_result ;
        copy_set_result = ImageGray(frame,1);
        copy_set_result = ImageBinary(copy_set_result, "inverted",80);
        copy_set_result = ImageComicMesh_Mix(copy_set_result, 1, 1,"normal","grad") ;   
        // 顯示影像
        cv::imshow("Original Video", frame);
        cv::imshow("Processed Video", copy_set_result);
        // 儲存處理後的影像
        writer.write(copy_set_result);
        if (div_output == 1){
            string output_image_name = "frame_div_" + std::to_string(idx) + ".jpeg";
            bool success = cv::imwrite(output_image_name, copy_set_result);
            if (success) {
                printf("Frame_Output = %d >> %s\n", idx + 1, output_image_name.c_str());
            } else {
                std::cerr << "無法儲存檔案: " << output_image_name << std::endl;
            }
            idx ++ ;
        }
        // 按 'q' 退出
        if (cv::waitKey(30) == 'q') break;
    }

    // 釋放資源
    cap.release();
    writer.release();
    cv::destroyAllWindows();
    std::cout << "影片處理完成，結果儲存於：" << outputVideoPath << std::endl;

}