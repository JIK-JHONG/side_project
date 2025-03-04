#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QWheelEvent>  // 包含 QWheelEvent 標頭檔案
#include <QGraphicsView>        // 包含 QGraphicsView
#include <QLineEdit>        // 包含 QGraphicsView
#include <QGraphicsPixmapItem>  // 包含 QGraphicsPixmapItem
#include <QLabel>        // 包含 QGraphicsView
#include <QCheckBox>        // 包含 QCheckBox
#include <QSlider>        // 包含 QSlider
#include <QRadioButton>        // 包含 QRadioButton
#include <QPushButton>        // 包含 QPushButton
#include <QProgressBar>        // 包含 QProgressBar
#include <opencv2/opencv.hpp>
namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = nullptr);
    ~MainWindow();

private slots:
    void loadImagesFromFolder();
    void updateImageValue(int value);  // 更新 二元閥值 數值
    int getImageValue();  // 更新 二元閥值 數值
    void updateImageValue_2(int value);  // 更新 二元閥值 數值
    int getImageValue_2();  // 更新 二元閥值 數值
    void updateScreentoneGapValue(int value);  // 更新 gap 的數值
    void updateScreentoneGapValue_2(int value);  // 更新 gap 的數值
    void updateScreentoneSizeValue(int value); // 更新 size 的數值
    // void updateOptionSet();  // 新增的方法來檢查 radio button 狀態
    void updateOptionCheck();  // 檢查 check box 狀態
    // int getOptionSet();  // 新增的方法來檢查 radio button 狀態
    int getOptionCheck();  // 檢查 check box 狀態

    void updateOptionCheck2();  // 檢查 check box 狀態
    int getOptionCheck2();  // 檢查 check box 狀態
    void updateOptionCheck3();  // 檢查 check box 狀態
    int getOptionCheck3();  // 檢查 check box 狀態

    void onResultButtonClicked();   // 輸出選擇
    int getScreentoneGapValue();
    int getScreentoneGapValue_2();
    int getScreentoneSizeValue();
    // int getOptionColorSet();
    // void updateOptionColorSet();
    int getbwrev_btnSet();
    void updateObwrev_btnSet();

    // void setupRadioButtonGroup();
    void updateProcessBar(int value);
    void updateGraphicsView(QGraphicsView *view, cv::Mat &image);

protected:
    void wheelEvent(QWheelEvent *event) override;  // 宣告 wheelEvent

private:
    Ui::MainWindow *ui;
    void fitImageToView(QGraphicsPixmapItem *item, QGraphicsView *view);
    QLineEdit *filePathInfo;  // 宣告 QLabel 用來顯示檔案路徑
    QLabel *image_w_val, *image_h_val, *image_c_val,*screenton_gap,*screenton_size, *image_threshold_val, *image_threshold_val_2, *label_time, *screenton_gap_2;
    // QRadioButton *radioBtn_0, *radioBtn_1, *radioBtn_2, *radioBtn_3;
    QSlider *Slider_screentone_gap, *Slider_screentone_size, *image_threshold,*image_threshold_2, *Slider_screentone_gap_2;
    QCheckBox *option_check, *option_check_2, *option_check_3;
    QPushButton *result,*bwrev_btn;
    QProgressBar *progressBar;
    // QLabel *image_w_val;
    // QLabel *image_h_val;
    // QLabel *image_c_val;
};

#endif // MAINWINDOW_H
