#include "mainwindow.h"
#include "ui_mainwindow.h"
#include "image_process.h"  // 引入影像處理檔案

#include <QGraphicsScene>
#include <QGraphicsPixmapItem>
#include <QFileDialog>
#include <QMessageBox>
#include <QDir>
#include <opencv2/opencv.hpp> // 引入 OpenCV 頭文件
#include <QWheelEvent>  // 添加這一行
#include <QIcon>
#include <QDebug>
#include <QSlider>
#include <QButtonGroup>
#include <QElapsedTimer>
// #include <QGraphicsPixmapItem>

MainWindow::MainWindow(QWidget *parent)
    : QMainWindow(parent)
    , ui(new Ui::MainWindow)
{
    ui->setupUi(this);
    // // 初始化 QSlider 範圍
    // Slider_Blur_Edge = new QSlider(Qt::Horizontal, this);
    // Slider_Binary_Threshold = new QSlider(Qt::Horizontal, this);

    ui->Slider_Blur_Edge->setRange(1, 255);  // 設定範圍：1 到 100
    ui->Slider_Binary_Threshold->setRange(0, 255);  // 設定範圍：5 到 50
    ui->Slider_Blur_Bks->setRange(0, 255);  // 設定範圍：5 到 50
    ui->Slider_Blur_Edge->setValue(1);
    ui->Slider_Binary_Threshold->setValue(80);
    ui->Slider_Blur_Bks->setValue(1);


    ui->image_threshold->setRange(0, 255);  // 設定範圍：5 到 50
    ui->image_threshold->setValue(0);  // 設定範圍：5 到 50
    ui->image_threshold_val->setText(QString::number(80));  // 設定範圍：5 到 50

    ui->image_threshold_2->setRange(1, 255);  // 設定範圍：5 到 50
    ui->image_threshold_2->setValue(80);  // 設定範圍：5 到 50
    ui->image_threshold_val_2->setText(QString::number(80));  // 設定範圍：5 到 50

    ui->progressBar->setMinimum(0);  // 設定最小值
    ui->progressBar->setMaximum(100); // 設定最大值
    ui->progressBar->setValue(0);   // 設定當前值

    // // 初始化 QLabel 來顯示數值
    // Slider_Blur_Edge_Val = new QLabel("1", this);
    // Slider_Binary_Threshold_Val = new QLabel("1", this);

    // 連接 Slider 的 valueChanged 訊號到槽函式
    connect(ui->Slider_Blur_Edge, &QSlider::valueChanged, this, &MainWindow::updateBlur_Edge);
    connect(ui->Slider_Blur_Bks, &QSlider::valueChanged, this, &MainWindow::updateBlur_Bks);
    connect(ui->Slider_Binary_Threshold, &QSlider::valueChanged, this, &MainWindow::updateBinary_Threshold);

    connect(ui->image_threshold, &QSlider::valueChanged, this, &MainWindow::updateImageValue);
    connect(ui->image_threshold_2, &QSlider::valueChanged, this, &MainWindow::updateImageValue_2);

    // setupRadioButtonGroup();
    // ui->radioBtn_0->setChecked(true);
    // ui->radioBtn_2->setChecked(true);
    // // 在 MainWindow 的構造函數中，假設你的按鈕名稱是 resultButton
    connect(ui->result, &QPushButton::clicked, this, &MainWindow::onResultButtonClicked);
    // 設定窗口標題
    setWindowTitle("景深模擬小工具");
    // 設定視// 設定圖標並檢查是否成功加載
    QIcon icon(":/src/images/icon.icns");
    if (icon.isNull()) {
        qDebug() << "Icon not found!";  // 如果圖標找不到，輸出訊息
    } else {
        qDebug() << "Icon is found!";  // 如果圖標找不到，輸出訊息
        setWindowIcon(icon);  // 如果成功找到，設置圖標窗的圖標
    }


    // setWindowIcon(QIcon(":/images/demo.png"));
    // 禁用 QGraphicsView 的默認滾輪縮放行為
    ui->view1->setInteractive(false);
    ui->view2->setInteractive(false);

    // 設置按鈕的點擊事件
    connect(ui->loadButton, &QPushButton::clicked, this, &MainWindow::loadImagesFromFolder);
}

MainWindow::~MainWindow()
{
    delete ui;
}

QImage cvMatToQImage(const Mat &mat) {
    // 如果是灰階圖像
    if (mat.channels() == 1) {
        return QImage(mat.data, mat.cols, mat.rows, mat.step, QImage::Format_Grayscale8);
    }
    // 如果是彩色圖像
    else if (mat.channels() == 3) {
        cvtColor(mat, mat, COLOR_BGR2RGB); // 轉換為 RGB
        return QImage(mat.data, mat.cols, mat.rows, mat.step, QImage::Format_RGB888);
    }
    return QImage();
}


void MainWindow::onResultButtonClicked() {
    ui->label_time->setText("0");
    QElapsedTimer timer;
    timer.start();  // 開始計時
    updateProcessBar(0);
    int auto_check = getbwrev_btnSet() ;
    // 1. 取得原始影像，這應該是從 loadImagesFromFolder 中選擇的圖片
    QString filePath = ui->filePathInfo->text(); // 假設這是選擇的圖片路徑

    // 使用 OpenCV 加載圖像
    cv::Mat img0 = cv::imread(filePath.toStdString(), cv::IMREAD_COLOR);
    cv::Mat copy_set = img0.clone();
    // cv::Mat copy_set = cv::imread(filePath.toStdString(), cv::IMREAD_COLOR);

    // 檢查圖片是否加載成功
    if (copy_set.empty()) {
        QMessageBox::warning(this, "Load Error", "Failed to load image: " + filePath);
        return;
    }
    qDebug() << "auto_check = " << auto_check;  // 如果圖標找不到，輸出訊息
    // 2. 使用 ImageGray 函數進行灰階處理
    copy_set = ImageGray(copy_set, 1); // 這裡是灰階選項

    // 3. 檢查影像的二值化顏色
    // int image_check = image_binary_color_check(copy_set, 80);
    int image_threshold = getImageValue();
    // qDebug() << "image_threshold = result " << image_threshold;  // 如果圖標找不到，輸出訊息
    if (auto_check == 1){
        int image_check = image_binary_color_check(copy_set, image_threshold);
        if (image_check == 1)
        {
            // printf("Run - ImageBinary - Normal\n");
            copy_set = ImageBinary(copy_set, "normal", image_threshold);
        }
        else
        {
            copy_set = ImageBinary(copy_set, "inverted", image_threshold);
            // printf("Run - ImageBinary - inverted\n");
        }
    }else{
            copy_set = ImageBinary(copy_set, "normal", image_threshold);
    }
    // 4. 混合影像效果

    int Binary_Threshold_Size = getBinary_Threshold();
    int Blur_Edge_Size = getBlur_Edge();
    int Blur_Bks_Size = getBlur_Bks();
    qDebug() << "Binary_Threshold_Size = " << Binary_Threshold_Size;  // 如果圖標找不到，輸出訊息
    qDebug() << "Blur_Edge_Size = " << Blur_Edge_Size;  // 如果圖標找不到，輸出訊息
    // std::string screentone_type = "normal";
    // std::string screentone_color = "grad";
    // int output_file_option = 0 ;

    // if (getOptionSet() == 0){
    //     screentone_type = "normal";
    // }else if(getOptionSet() == 1){
    //     screentone_type = "square";
    // }
    // if (getOptionColorSet() == 0){
    //     screentone_color = "grad";
    //     copy_set = ImageBinary(copy_set, "normal", 80);
    // }else if(getOptionColorSet() == 1){
    //     screentone_color = "std";
    // }

    int image_threshold_2 = getImageValue_2();
    // qDebug() << "screentone_color = " << screentone_color;  // 如果圖標找不到，輸出訊息
    // cv::Mat copy_set_result = ImageComicMesh_Mix(copy_set, Binary_Threshold_Size, Blur_Edge_Size, screentone_type, screentone_color);

    qDebug() << "image_threshold = " << image_threshold;  // 如果圖標找不到，輸出訊息
    qDebug() << "image_threshold_2 = " << image_threshold_2;  // 如果圖標找不到，輸出訊息
    copy_set = cv::imread(filePath.toStdString(), cv::IMREAD_COLOR);
    copy_set = ImageGray(copy_set, 1); // 這裡是灰階選項
    int img_revise_select = 0 ;
    if (ui->option_check_2->isChecked()){
        img_revise_select = 1;

    }
    qDebug() << "[]img_revise_select = " << img_revise_select;  // 如果圖標找不到，輸出訊息
    cv::Mat copy_set_result = Image_Test_Canny(copy_set,img0,Binary_Threshold_Size,Blur_Edge_Size,image_threshold,image_threshold_2,getbwrev_btnSet(),img_revise_select,getOptionCheck3(),Blur_Bks_Size);

    // copy_set = ImageComicMesh_Mix(copy_set, 1, 1, "square", "std");

    // 5. 顯示處理後的影像到 view2

    // QImage qimg = cvMatToQImage(copy_set_result); // 假設你已經寫了這個函數來轉換 OpenCV 的 Mat 到 QImage

    // 先清除現有的場景（如果已經有場景的話）
    ui->view2->setScene(nullptr);  // 移除原場景
    updateGraphicsView(ui->view2, copy_set_result);
    // // 創建 QGraphicsScene 和 QPixmap
    // QGraphicsScene *scene = new QGraphicsScene(this);
    // // QPixmap pixmap = QPixmap::fromImage(qimg); // 從 QImage 創建 QPixmap


    // // // 設置 QGraphicsView 的場景
    // // ui->view1->setScene(scene1);
    // // ui->view2->setScene(scene2);

    // // // 將 OpenCV 的 Mat 轉換為 QImage
    // // QImage qimg(img.data, img.cols, img.rows, img.step, QImage::Format_BGR888);

    // // // 將 QImage 轉換為 QPixmap
    // // QPixmap pixmap = QPixmap::fromImage(qimg);

    // // // 創建 QGraphicsPixmapItem 並設置圖片
    // // QGraphicsPixmapItem *item1 = new QGraphicsPixmapItem(pixmap);
    // // scene1->addItem(item1);

    // // // 在 view2 中顯示灰階圖像
    // // cv::Mat grayImg;
    // // grayImg = ImageGray(img);



    // QImage qimg(copy_set_result.data, copy_set_result.cols, copy_set_result.rows, copy_set_result.step, QImage::Format_BGR888);
    // // 將 QImage 轉換為 QPixmap
    // QPixmap pixmap = QPixmap::fromImage(qimg);
    // QGraphicsPixmapItem *item = new QGraphicsPixmapItem(pixmap); // 創建圖像項目



    // // 將圖像項目添加到場景
    // scene->addItem(item);

    // // 設定視圖場景
    // ui->view2->setScene(scene);

    // // 使用原來的 fitImageToView 函數，將 QGraphicsPixmapItem 傳入
    // fitImageToView(item, ui->view2);  // 呼叫這個函數進行縮放

    // ui->view2->update();  // 強制刷新視圖
    // 更新視圖範圍
    updateProcessBar(100);
    // 6. 檢查是否需要儲存圖檔
    if (ui->option_check->isChecked()) {
        // 取得檔案名稱與副檔名
        QString savePath = ui->filePathInfo->text();  // 使用 text() 獲取輸入的路徑
        QFileInfo fileInfo(savePath);
        QString originalFileName = fileInfo.baseName();  // 原始檔名（不含副檔名）

        // 如果 filePathInfo 設定了檔案路徑，可以從這裡取得作為基礎檔案名稱
        QString baseFileName = ui->filePathInfo->text(); // 假設這裡有路徑資訊
        qDebug() << "baseFileName = "<< baseFileName;  // 如果圖標找不到，輸出訊息
        if (!baseFileName.isEmpty()) {
            // 取得原始檔案名稱（不包含路徑）
            QFileInfo baseFileInfo(baseFileName);
            originalFileName = baseFileInfo.baseName();  // 原始檔名
        }

        // 新的檔名加上 "_modified" 並設定為 .jpeg 格式
        QString newFileName = originalFileName + "_modified.jpeg";
        QString finalSavePath = fileInfo.absolutePath() + "/" + newFileName;

        // 直接儲存圖像，無需讓使用者選擇檔案名稱
        cvtColor(copy_set_result,copy_set_result,cv::COLOR_BGR2RGB);
        bool success = cv::imwrite(finalSavePath.toStdString(), copy_set_result);

        // 檢查儲存結果，並顯示對話框通知使用者
        // if (finalSavePath.isEmpty()) {
        //     qDebug() << "Error: finalSavePath is empty!";
        //     return;
        // }
        // 下面視窗顯示會有問題（如果透過QT IDE）。
        if (success) {
            QMessageBox::information(this, "儲存完成", "圖像已成功儲存到：" + finalSavePath);
            // QMessageBox::information(nullptr, "儲存完成", "圖像已成功儲存到：" + finalSavePath);
            // QMessageBox::information();
        } else {
            QMessageBox::warning(this, "儲存失敗", "無法儲存圖像到：" + finalSavePath);
            // QMessageBox::warning(nullptr, "儲存失敗", "無法儲存圖像到：" + finalSavePath);
        }
    }
    qint64 elapsedTime = timer.elapsed();
    ui->label_time->setText(QString::number(elapsedTime / 1000.0, 'f', 3));

}
// 在建構子或初始化函式中設置
// void MainWindow::setupRadioButtonGroup()
// {
//     // 創建 QButtonGroup 物件
//     QButtonGroup* group1 = new QButtonGroup(this);
//     QButtonGroup* group2 = new QButtonGroup(this);

//     // 把 radio buttons 添加到對應的 QButtonGroup 中
//     group1->addButton(ui->radioBtn_0);
//     group1->addButton(ui->radioBtn_1);

//     group2->addButton(ui->radioBtn_2);
//     group2->addButton(ui->radioBtn_3);

//     // 設定第一組預設選中 radioBtn_0
//     ui->radioBtn_0->setChecked(true);

//     // 設定第二組預設選中 radioBtn_2
//     ui->radioBtn_3->setChecked(true);
// }


// 根據 radioBtn_2 和 radioBtn_3 的選擇狀態返回對應的選項
// int MainWindow::getOptionColorSet() {
//     if (ui->radioBtn_2->isChecked()) {
//         qDebug() << "Radio button 2 is selected!";
//         return 1; // 如果 radioBtn_2 被選中，回傳 0
//     } else if (ui->radioBtn_3->isChecked()) {
//         qDebug() << "Radio button 3 is selected!";
//         return 0; // 如果 radioBtn_3 被選中，回傳 1
//     }
//     return -1; // 若兩者都未選中，回傳 -1
// }

// // 更新 radioBtn_2 和 radioBtn_3 的選擇狀態
// void MainWindow::updateOptionColorSet() {
//     if (ui->radioBtn_2->isChecked()) {
//         qDebug() << "Radio button 2 is selected!";
//     } else if (ui->radioBtn_3->isChecked()) {
//         qDebug() << "Radio button 3 is selected!";
//     }
// }

// // 根據 radioBtn_0 和 radioBtn_1 的選擇狀態返回對應的選項
// int MainWindow::getOptionSet() {
//     if (ui->radioBtn_0->isChecked()) {
//         qDebug() << "Radio button 0 is selected!";
//         return 0; // 如果 radioBtn_0 被選中，回傳 0
//     } else if (ui->radioBtn_1->isChecked()) {
//         qDebug() << "Radio button 1 is selected!";
//         return 1; // 如果 radioBtn_1 被選中，回傳 1
//     }
//     return -1; // 若兩者都未選中，回傳 -1
// }

// // 更新 radioBtn_0 和 radioBtn_1 的選擇狀態
// void MainWindow::updateOptionSet() {
//     if (ui->radioBtn_0->isChecked()) {
//         qDebug() << "Radio button 0 is selected!";
//     } else if (ui->radioBtn_1->isChecked()) {
//         qDebug() << "Radio button 1 is selected!";
//     }
// }
void MainWindow::updateOptionCheck()
{
    // 檢查 option_check 的選擇狀態
    if (ui->option_check->isChecked()) {
        qDebug() << "Option check is selected!";
    } else {
        qDebug() << "Option check is not selected.";
    }
}
int MainWindow::getOptionCheck()
{
    int check_status = 0 ;
    // 檢查 option_check 的選擇狀態
    if (ui->option_check->isChecked()) {
        check_status = 1 ;
        qDebug() << "Option check is selected!";
    } else {
        check_status = 0 ;
        qDebug() << "Option check is not selected.";
    }
    return check_status;
}

void MainWindow::updateOptionCheck2()
{
    // 檢查 option_check 的選擇狀態
    if (ui->option_check_2->isChecked()) {
        qDebug() << "Option check is selected!";
    } else {
        qDebug() << "Option check is not selected.";
    }
}
int MainWindow::getOptionCheck2()
{
    int check_status = 0 ;
    // 檢查 option_check 的選擇狀態
    if (ui->option_check_2->isChecked()) {
        check_status = 1 ;
        qDebug() << "Option check is selected!";
    } else {
        check_status = 0 ;
        qDebug() << "Option check is not selected.";
    }
    return check_status;
}

void MainWindow::updateOptionCheck3()
{
    // 檢查 option_check 的選擇狀態
    if (ui->option_check_binary->isChecked()) {
        qDebug() << "Option check is selected!";
    } else {
        qDebug() << "Option check is not selected.";
    }
}
int MainWindow::getOptionCheck3()
{
    int check_status = 0 ;
    // 檢查 option_check 的選擇狀態
    if (ui->option_check_binary->isChecked()) {
        check_status = 1 ;
        qDebug() << "Option check is selected!";
    } else {
        check_status = 0 ;
        qDebug() << "Option check is not selected.";
    }
    return check_status;
}
void MainWindow::updateObwrev_btnSet()
{
    // 檢查 option_check 的選擇狀態
    if (ui->bwrev_btn->isChecked()) {
        qDebug() << "Option check is selected!";
    } else {
        qDebug() << "Option check is not selected.";
    }
}
int MainWindow::getbwrev_btnSet()
{
    int check_status = 0 ;
    // 檢查 option_check 的選擇狀態
    if (ui->bwrev_btn->isChecked()) {
        check_status = 1 ;
        qDebug() << "Option check is selected!";
    } else {
        check_status = 0 ;
        qDebug() << "Option check is not selected.";
    }
    return check_status;
}
// 更新 影像閥值 值
int MainWindow::getImageValue() {
    return ui->image_threshold->value(); // 正確取得並返回數值
}
void MainWindow::updateImageValue(int value)
{
    updateProcessBar(0);

    ui->image_threshold_val->setText(QString::number(value));  // 更新 QLabel 顯示數值
    // qDebug() << "image_threshold_val = " << value;

    // QString filePath = ui->filePathInfo->text();
    // if (filePath.isEmpty()) {
    //     qDebug() << "Error: File path is empty!";
    //     return;
    // }

    // // 使用 OpenCV 加載圖像
    // cv::Mat img = cv::imread(filePath.toStdString(), cv::IMREAD_COLOR);
    // if (img.empty()) {
    //     qDebug() << "Error: Failed to load image!";
    //     return;
    // }

    // // 轉換為灰階
    // cv::Mat grayImg = ImageGray(img);

    // int image_threshold = getImageValue();
    // int auto_check = getbwrev_btnSet();
    // qDebug() << "auto_check = refresh >>>> " << auto_check;

    // if (auto_check == 1) {
    //     int image_check = image_binary_color_check(grayImg, image_threshold);
    //     if (image_check == 1) {
    //         grayImg = ImageBinary(grayImg, "normal", image_threshold);
    //     } else {
    //         grayImg = ImageBinary(grayImg, "inverted", image_threshold);
    //     }
    // } else {
    //     grayImg = ImageBinary(grayImg, "normal", image_threshold);
    // }

    // // 清除舊場景（防止記憶體洩漏）
    // if (ui->view2->scene()) {
    //     delete ui->view2->scene();
    // }
    // updateGraphicsView(ui->view2, grayImg);
    onResultButtonClicked();
    updateProcessBar(100);
}

// 更新 影像閥值 值
int MainWindow::getImageValue_2() {
    return ui->image_threshold_2->value(); // 正確取得並返回數值
}
void MainWindow::updateImageValue_2(int value)
{
    updateProcessBar(0);

    ui->image_threshold_val_2->setText(QString::number(value));  // 更新 QLabel 顯示數值
    // qDebug() << "image_threshold_val = " << value;

    // QString filePath = ui->filePathInfo->text();
    // if (filePath.isEmpty()) {
    //     qDebug() << "Error: File path is empty!";
    //     return;
    // }

    // // 使用 OpenCV 加載圖像
    // cv::Mat img = cv::imread(filePath.toStdString(), cv::IMREAD_COLOR);
    // if (img.empty()) {
    //     qDebug() << "Error: Failed to load image!";
    //     return;
    // }

    // // 轉換為灰階
    // cv::Mat grayImg = ImageGray(img);

    // int image_threshold = getImageValue();
    // int auto_check = getbwrev_btnSet();
    // qDebug() << "auto_check = refresh >>>> " << auto_check;

    // if (auto_check == 1) {
    //     int image_check = image_binary_color_check(grayImg, image_threshold);
    //     if (image_check == 1) {
    //         grayImg = ImageBinary(grayImg, "normal", image_threshold);
    //     } else {
    //         grayImg = ImageBinary(grayImg, "inverted", image_threshold);
    //     }
    // } else {
    //     grayImg = ImageBinary(grayImg, "normal", image_threshold);
    // }

    // // 清除舊場景（防止記憶體洩漏）
    // if (ui->view2->scene()) {
    //     delete ui->view2->scene();
    // }
    // updateGraphicsView(ui->view2, grayImg);
    onResultButtonClicked();
    updateProcessBar(100);
}


void MainWindow::updateGraphicsView(QGraphicsView *view, cv::Mat &image) {
    // 建立新的場景
    QGraphicsScene *scene = new QGraphicsScene(this);

    // OpenCV BGR to RGB 轉換（避免顏色錯誤）
    cv::cvtColor(image, image, cv::COLOR_BGR2RGB);

    // 將 OpenCV Mat 轉為 QImage
    QImage qimg(image.data, image.cols, image.rows, image.step, QImage::Format_RGB888);

    // 將 QImage 轉換為 QPixmap
    QPixmap pixmap = QPixmap::fromImage(qimg);
    QGraphicsPixmapItem *item = new QGraphicsPixmapItem(pixmap);

    // 添加圖像到場景
    scene->addItem(item);
    view->setScene(scene);

    // 確保影像適應 QGraphicsView
    fitImageToView(item, view);
    view->setSceneRect(scene->itemsBoundingRect());
}

void MainWindow::updateProcessBar(int value){
    value = qBound(0, value, 100);  // 限制數值範圍
    // qDebug() << "updateProcessBar" << value;
    qDebug() << "updateProcessBar(" << value << ") executed, actual progressBar value:" << ui->progressBar->value();
    ui->progressBar->setValue(value);
}
// 更新 Gap 值
int MainWindow::getBlur_Edge() {
    return ui->Slider_Blur_Edge->value(); // 正確取得並返回數值
}
void MainWindow::updateBlur_Edge(int value)
{
    ui->Slider_Blur_Edge_Val->setText(QString::number(value));  // 使用 setText 更新 QLabel
    qDebug() << "Slider_Blur_Edge_Val = " <<QString::number(value);
    onResultButtonClicked();
}
int MainWindow::getBlur_Bks() {
    return ui->Slider_Blur_Bks->value(); // 正確取得並返回數值
}
void MainWindow::updateBlur_Bks(int value)
{
    ui->Slider_Blur_Bks_Val->setText(QString::number(value));  // 使用 setText 更新 QLabel
    qDebug() << "Slider_Blur_Bks_Val = " <<QString::number(value);
    onResultButtonClicked();
}

int MainWindow::getBinary_Threshold() {
    return ui->Slider_Binary_Threshold->value(); // 正確取得並返回數值
}
// 更新 Size 值
void MainWindow::updateBinary_Threshold(int value)
{
    ui->Slider_Binary_Threshold_Val->setText(QString::number(value));  // 使用 setText 更新 QLabel
    qDebug() << "Slider_Binary_Threshold_Val = " <<QString::number(value);
    onResultButtonClicked();
}
// 縮放圖片以適應視圖大小
void MainWindow::fitImageToView(QGraphicsPixmapItem *item, QGraphicsView *view)
{
    // 獲取圖片的寬高

    QPixmap pixmap = item->pixmap();
    QImage image = pixmap.toImage();
    QString Image_Type = "-";
    qDebug() << "Image size:" << image.width() << "x" << image.height();

    switch (image.format()) {
    case QImage::Format_Mono:
    case QImage::Format_MonoLSB:
        Image_Type = "Black&White";
        qDebug() << "Channel count: 1 (Black & White)";
        break;
    case QImage::Format_Indexed8:
        Image_Type = "Gray";
        qDebug() << "Channel count: 1 (Grayscale)";
        break;
    case QImage::Format_RGB32:
        Image_Type = "RGB";
        break;
    case QImage::Format_ARGB32:
        Image_Type = "RGBA";
        break;
    case QImage::Format_ARGB32_Premultiplied:
        Image_Type = "RGBA";
        qDebug() << "Channel count: 4 (RGBA)";
        break;
    case QImage::Format_RGB888:
        Image_Type = "RGB";
        qDebug() << "Channel count: 3 (RGB)";
        break;
    default:
        qDebug() << "Unknown format";
        break;
    }


    QSizeF imageSize = item->pixmap().size();

    ui->image_w_val->setText(QString::number(imageSize.width()));
    ui->image_h_val->setText(QString::number(imageSize.height()));
    ui->image_c_val->setText(Image_Type);


    QSizeF viewSize = view->viewport()->size();

    // 計算縮放比例
    qreal scaleFactor = qMin(viewSize.width() / imageSize.width(), viewSize.height() / imageSize.height());

    // 設置縮放
    item->setScale(scaleFactor);
}

void MainWindow::loadImagesFromFolder()
{
    updateProcessBar(0);
    // 打開文件對話框選擇單一圖片檔案，並過濾支援的格式
    QString filePath = QFileDialog::getOpenFileName(this, "Open Image", "",
                                                    "Images (*.png *.jpg *.jpeg *.bmp)");

    // 如果選擇了有效的圖片檔案
    if (!filePath.isEmpty())
    {
        // 更新 QLineEdit 顯示的文字
        ui->filePathInfo->setText(filePath);
        // 使用 OpenCV 加載圖像
        cv::Mat img = cv::imread(filePath.toStdString(), cv::IMREAD_COLOR);

        // 檢查圖片是否加載成功
        if (img.empty()) {
            QMessageBox::warning(this, "Load Error", "Failed to load image: " + filePath);
            return;
        }
        updateProcessBar(0);
        // 創建場景
        QGraphicsScene *scene1 = new QGraphicsScene(this);
        QGraphicsScene *scene2 = new QGraphicsScene(this);

        // 設置 QGraphicsView 的場景
        ui->view1->setScene(scene1);
        ui->view2->setScene(scene2);

        // 將 OpenCV 的 Mat 轉換為 QImage
        QImage qimg(img.data, img.cols, img.rows, img.step, QImage::Format_BGR888);

        // 將 QImage 轉換為 QPixmap
        QPixmap pixmap = QPixmap::fromImage(qimg);

        // 創建 QGraphicsPixmapItem 並設置圖片
        QGraphicsPixmapItem *item1 = new QGraphicsPixmapItem(pixmap);
        scene1->addItem(item1);

        // 在 view2 中顯示灰階圖像

        // cv::Mat grayImg;
        // grayImg = ImageGray(img);
        // // cv::cvtColor(img, grayImg, cv::COLOR_BGR2GRAY);  // 轉換為灰階

        // int image_threshold = getImageValue();
        // int auto_check = getbwrev_btnSet() ;
        // qDebug() << "auto_check =" << auto_check;
        // if (auto_check == 1){
        //     int image_check = image_binary_color_check(grayImg, image_threshold);
        //     if (image_check == 1)
        //     {
        //         grayImg = ImageBinary(grayImg, "normal", image_threshold);
        //     }
        //     else
        //     {
        //         grayImg = ImageBinary(grayImg, "inverted", image_threshold);
        //     }
        // }else{
        //     // if (getOptionColorSet() == 0){
        //         grayImg = ImageBinary(grayImg, "normal", image_threshold);
        //     // }
        // }

        onResultButtonClicked();

        // // 將灰階圖像轉換為 QImage
        // QImage grayQimg(grayImg.data, grayImg.cols, grayImg.rows, grayImg.step, QImage::Format_BGR888);

        // // 將 QImage 轉換為 QPixmap
        // QPixmap grayPixmap = QPixmap::fromImage(grayQimg);

        // // 創建 QGraphicsPixmapItem 並設置灰階圖像
        // QGraphicsPixmapItem *item2 = new QGraphicsPixmapItem(grayPixmap);
        // scene2->addItem(item2);

        // 設置初始縮放比例：使圖片適合視圖大小
        fitImageToView(item1, ui->view1);
        // fitImageToView(item2, ui->view2);

        // 更新視圖範圍
        updateProcessBar(100);
        ui->view1->setSceneRect(scene1->itemsBoundingRect());
        // ui->view2->setSceneRect(scene2->itemsBoundingRect());
    }
}

// 處理縮放事件
void MainWindow::wheelEvent(QWheelEvent *event)
{
    // 防止滾輪事件觸發縮放操作
    event->accept();  // 或者不執行任何操作
}
