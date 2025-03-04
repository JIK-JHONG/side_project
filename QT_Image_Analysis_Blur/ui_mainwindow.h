/********************************************************************************
** Form generated from reading UI file 'mainwindow.ui'
**
** Created by: Qt User Interface Compiler version 6.8.2
**
** WARNING! All changes made in this file will be lost when recompiling UI file!
********************************************************************************/

#ifndef UI_MAINWINDOW_H
#define UI_MAINWINDOW_H

#include <QtCore/QVariant>
#include <QtWidgets/QApplication>
#include <QtWidgets/QCheckBox>
#include <QtWidgets/QGraphicsView>
#include <QtWidgets/QGroupBox>
#include <QtWidgets/QLabel>
#include <QtWidgets/QLineEdit>
#include <QtWidgets/QMainWindow>
#include <QtWidgets/QMenuBar>
#include <QtWidgets/QProgressBar>
#include <QtWidgets/QPushButton>
#include <QtWidgets/QSlider>
#include <QtWidgets/QStatusBar>
#include <QtWidgets/QWidget>

QT_BEGIN_NAMESPACE

class Ui_MainWindow
{
public:
    QWidget *centralwidget;
    QLabel *title_info;
    QPushButton *loadButton;
    QLineEdit *filePathInfo;
    QGraphicsView *view1;
    QGraphicsView *view2;
    QPushButton *result;
    QCheckBox *option_check;
    QProgressBar *progressBar;
    QGroupBox *groupBox;
    QSlider *image_threshold;
    QLabel *image_threshold_val;
    QSlider *image_threshold_2;
    QLabel *image_threshold_val_2;
    QLabel *label_4;
    QLabel *label_6;
    QCheckBox *bwrev_btn;
    QGroupBox *groupBox_2;
    QLabel *label;
    QSlider *Slider_screentone_size;
    QLabel *screenton_size;
    QLabel *label_2;
    QSlider *Slider_screentone_gap;
    QLabel *screenton_gap;
    QCheckBox *option_check_2;
    QSlider *Slider_screentone_gap_2;
    QLabel *screenton_gap_2;
    QLabel *label_5;
    QGroupBox *groupBox_3;
    QCheckBox *option_check_3;
    QGroupBox *groupBox_4;
    QLabel *image_w;
    QLabel *image_h;
    QLabel *image_c;
    QLabel *image_h_val;
    QLabel *image_c_val;
    QLabel *image_w_val;
    QLabel *label_3;
    QLabel *label_time;
    QLabel *label_7;
    QMenuBar *menubar;
    QStatusBar *statusbar;

    void setupUi(QMainWindow *MainWindow)
    {
        if (MainWindow->objectName().isEmpty())
            MainWindow->setObjectName("MainWindow");
        MainWindow->resize(970, 692);
        centralwidget = new QWidget(MainWindow);
        centralwidget->setObjectName("centralwidget");
        title_info = new QLabel(centralwidget);
        title_info->setObjectName("title_info");
        title_info->setGeometry(QRect(20, 20, 71, 31));
        title_info->setAlignment(Qt::AlignmentFlag::AlignCenter);
        loadButton = new QPushButton(centralwidget);
        loadButton->setObjectName("loadButton");
        loadButton->setGeometry(QRect(670, 10, 100, 51));
        filePathInfo = new QLineEdit(centralwidget);
        filePathInfo->setObjectName("filePathInfo");
        filePathInfo->setGeometry(QRect(130, 20, 521, 31));
        QFont font;
        font.setItalic(true);
        filePathInfo->setFont(font);
        view1 = new QGraphicsView(centralwidget);
        view1->setObjectName("view1");
        view1->setGeometry(QRect(20, 80, 371, 481));
        view2 = new QGraphicsView(centralwidget);
        view2->setObjectName("view2");
        view2->setGeometry(QRect(400, 80, 371, 481));
        result = new QPushButton(centralwidget);
        result->setObjectName("result");
        result->setGeometry(QRect(790, 550, 161, 61));
        option_check = new QCheckBox(centralwidget);
        option_check->setObjectName("option_check");
        option_check->setGeometry(QRect(790, 530, 151, 20));
        progressBar = new QProgressBar(centralwidget);
        progressBar->setObjectName("progressBar");
        progressBar->setGeometry(QRect(20, 570, 561, 31));
        progressBar->setValue(24);
        groupBox = new QGroupBox(centralwidget);
        groupBox->setObjectName("groupBox");
        groupBox->setGeometry(QRect(790, 370, 171, 151));
        image_threshold = new QSlider(groupBox);
        image_threshold->setObjectName("image_threshold");
        image_threshold->setGeometry(QRect(10, 40, 111, 25));
        image_threshold->setOrientation(Qt::Orientation::Horizontal);
        image_threshold_val = new QLabel(groupBox);
        image_threshold_val->setObjectName("image_threshold_val");
        image_threshold_val->setGeometry(QRect(120, 40, 41, 20));
        QFont font1;
        font1.setBold(true);
        image_threshold_val->setFont(font1);
        image_threshold_val->setAlignment(Qt::AlignmentFlag::AlignCenter);
        image_threshold_2 = new QSlider(groupBox);
        image_threshold_2->setObjectName("image_threshold_2");
        image_threshold_2->setGeometry(QRect(10, 90, 111, 25));
        image_threshold_2->setOrientation(Qt::Orientation::Horizontal);
        image_threshold_val_2 = new QLabel(groupBox);
        image_threshold_val_2->setObjectName("image_threshold_val_2");
        image_threshold_val_2->setGeometry(QRect(120, 90, 41, 20));
        image_threshold_val_2->setFont(font1);
        image_threshold_val_2->setAlignment(Qt::AlignmentFlag::AlignCenter);
        label_4 = new QLabel(groupBox);
        label_4->setObjectName("label_4");
        label_4->setGeometry(QRect(10, 20, 111, 16));
        QFont font2;
        font2.setPointSize(14);
        font2.setBold(true);
        label_4->setFont(font2);
        label_6 = new QLabel(groupBox);
        label_6->setObjectName("label_6");
        label_6->setGeometry(QRect(10, 70, 111, 16));
        label_6->setFont(font2);
        bwrev_btn = new QCheckBox(groupBox);
        bwrev_btn->setObjectName("bwrev_btn");
        bwrev_btn->setGeometry(QRect(10, 120, 151, 20));
        groupBox_2 = new QGroupBox(centralwidget);
        groupBox_2->setObjectName("groupBox_2");
        groupBox_2->setGeometry(QRect(790, 110, 171, 201));
        label = new QLabel(groupBox_2);
        label->setObjectName("label");
        label->setGeometry(QRect(10, 20, 121, 16));
        QFont font3;
        font3.setPointSize(14);
        font3.setBold(true);
        font3.setUnderline(false);
        label->setFont(font3);
        Slider_screentone_size = new QSlider(groupBox_2);
        Slider_screentone_size->setObjectName("Slider_screentone_size");
        Slider_screentone_size->setGeometry(QRect(10, 40, 111, 25));
        Slider_screentone_size->setOrientation(Qt::Orientation::Horizontal);
        screenton_size = new QLabel(groupBox_2);
        screenton_size->setObjectName("screenton_size");
        screenton_size->setGeometry(QRect(120, 40, 41, 20));
        screenton_size->setFont(font1);
        screenton_size->setAlignment(Qt::AlignmentFlag::AlignCenter);
        label_2 = new QLabel(groupBox_2);
        label_2->setObjectName("label_2");
        label_2->setGeometry(QRect(10, 70, 151, 16));
        label_2->setFont(font2);
        Slider_screentone_gap = new QSlider(groupBox_2);
        Slider_screentone_gap->setObjectName("Slider_screentone_gap");
        Slider_screentone_gap->setGeometry(QRect(10, 90, 111, 25));
        Slider_screentone_gap->setOrientation(Qt::Orientation::Horizontal);
        screenton_gap = new QLabel(groupBox_2);
        screenton_gap->setObjectName("screenton_gap");
        screenton_gap->setGeometry(QRect(120, 90, 41, 20));
        screenton_gap->setFont(font1);
        screenton_gap->setAlignment(Qt::AlignmentFlag::AlignCenter);
        option_check_2 = new QCheckBox(groupBox_2);
        option_check_2->setObjectName("option_check_2");
        option_check_2->setGeometry(QRect(10, 170, 151, 20));
        Slider_screentone_gap_2 = new QSlider(groupBox_2);
        Slider_screentone_gap_2->setObjectName("Slider_screentone_gap_2");
        Slider_screentone_gap_2->setGeometry(QRect(10, 140, 111, 25));
        Slider_screentone_gap_2->setOrientation(Qt::Orientation::Horizontal);
        screenton_gap_2 = new QLabel(groupBox_2);
        screenton_gap_2->setObjectName("screenton_gap_2");
        screenton_gap_2->setGeometry(QRect(120, 140, 41, 20));
        screenton_gap_2->setFont(font1);
        screenton_gap_2->setAlignment(Qt::AlignmentFlag::AlignCenter);
        label_5 = new QLabel(groupBox_2);
        label_5->setObjectName("label_5");
        label_5->setGeometry(QRect(10, 120, 151, 16));
        label_5->setFont(font2);
        groupBox_3 = new QGroupBox(centralwidget);
        groupBox_3->setObjectName("groupBox_3");
        groupBox_3->setGeometry(QRect(790, 310, 171, 61));
        option_check_3 = new QCheckBox(groupBox_3);
        option_check_3->setObjectName("option_check_3");
        option_check_3->setGeometry(QRect(10, 30, 151, 20));
        groupBox_4 = new QGroupBox(centralwidget);
        groupBox_4->setObjectName("groupBox_4");
        groupBox_4->setGeometry(QRect(790, 10, 171, 101));
        image_w = new QLabel(groupBox_4);
        image_w->setObjectName("image_w");
        image_w->setGeometry(QRect(10, 30, 58, 16));
        image_h = new QLabel(groupBox_4);
        image_h->setObjectName("image_h");
        image_h->setGeometry(QRect(10, 50, 58, 16));
        image_c = new QLabel(groupBox_4);
        image_c->setObjectName("image_c");
        image_c->setGeometry(QRect(10, 70, 58, 16));
        image_h_val = new QLabel(groupBox_4);
        image_h_val->setObjectName("image_h_val");
        image_h_val->setGeometry(QRect(70, 50, 91, 16));
        image_h_val->setFont(font1);
        image_h_val->setAlignment(Qt::AlignmentFlag::AlignCenter);
        image_c_val = new QLabel(groupBox_4);
        image_c_val->setObjectName("image_c_val");
        image_c_val->setGeometry(QRect(70, 70, 91, 16));
        image_c_val->setFont(font1);
        image_c_val->setAlignment(Qt::AlignmentFlag::AlignCenter);
        image_w_val = new QLabel(groupBox_4);
        image_w_val->setObjectName("image_w_val");
        image_w_val->setGeometry(QRect(70, 30, 91, 16));
        image_w_val->setFont(font1);
        image_w_val->setAlignment(Qt::AlignmentFlag::AlignCenter);
        label_3 = new QLabel(centralwidget);
        label_3->setObjectName("label_3");
        label_3->setGeometry(QRect(590, 570, 58, 31));
        label_time = new QLabel(centralwidget);
        label_time->setObjectName("label_time");
        label_time->setGeometry(QRect(650, 570, 81, 31));
        label_time->setFont(font1);
        label_time->setAlignment(Qt::AlignmentFlag::AlignCenter);
        label_7 = new QLabel(centralwidget);
        label_7->setObjectName("label_7");
        label_7->setGeometry(QRect(750, 570, 31, 31));
        MainWindow->setCentralWidget(centralwidget);
        menubar = new QMenuBar(MainWindow);
        menubar->setObjectName("menubar");
        menubar->setGeometry(QRect(0, 0, 970, 43));
        MainWindow->setMenuBar(menubar);
        statusbar = new QStatusBar(MainWindow);
        statusbar->setObjectName("statusbar");
        MainWindow->setStatusBar(statusbar);

        retranslateUi(MainWindow);

        QMetaObject::connectSlotsByName(MainWindow);
    } // setupUi

    void retranslateUi(QMainWindow *MainWindow)
    {
        MainWindow->setWindowTitle(QCoreApplication::translate("MainWindow", "MainWindow", nullptr));
        title_info->setText(QCoreApplication::translate("MainWindow", "\346\252\224\346\241\210\350\267\257\345\276\221", nullptr));
        loadButton->setText(QCoreApplication::translate("MainWindow", "\351\201\270\346\223\207\346\252\224\346\241\210", nullptr));
        result->setText(QCoreApplication::translate("MainWindow", "\345\237\267\350\241\214\351\201\213\347\256\227", nullptr));
        option_check->setText(QCoreApplication::translate("MainWindow", "\350\274\270\345\207\272\346\252\224\346\241\210", nullptr));
        groupBox->setTitle(QCoreApplication::translate("MainWindow", "\345\276\256\350\252\277", nullptr));
        image_threshold_val->setText(QCoreApplication::translate("MainWindow", "1", nullptr));
        image_threshold_val_2->setText(QCoreApplication::translate("MainWindow", "1", nullptr));
        label_4->setText(QCoreApplication::translate("MainWindow", "\351\253\230\346\226\257\346\250\241\347\263\212", nullptr));
        label_6->setText(QCoreApplication::translate("MainWindow", "\351\226\213\351\201\213\347\256\227\345\244\247\345\260\217", nullptr));
        bwrev_btn->setText(QCoreApplication::translate("MainWindow", "\345\217\215\345\220\221\351\201\213\347\256\227\357\274\210\351\226\211->\351\226\213\357\274\211", nullptr));
        groupBox_2->setTitle(QCoreApplication::translate("MainWindow", "\351\226\245\345\200\274\350\250\255\345\256\232", nullptr));
        label->setText(QCoreApplication::translate("MainWindow", "\344\272\214\351\232\216\345\214\226\351\226\245\345\200\274", nullptr));
        screenton_size->setText(QCoreApplication::translate("MainWindow", "1", nullptr));
        label_2->setText(QCoreApplication::translate("MainWindow", "\351\202\212\347\267\243\346\250\241\347\263\212\345\200\274", nullptr));
        screenton_gap->setText(QCoreApplication::translate("MainWindow", "1", nullptr));
        option_check_2->setText(QCoreApplication::translate("MainWindow", "\345\217\215\345\220\221\351\201\270\345\217\226", nullptr));
        screenton_gap_2->setText(QCoreApplication::translate("MainWindow", "1", nullptr));
        label_5->setText(QCoreApplication::translate("MainWindow", "\350\203\214\346\231\257\346\250\241\347\263\212\345\200\274", nullptr));
        groupBox_3->setTitle(QCoreApplication::translate("MainWindow", "\351\201\216\347\250\213\351\241\257\347\244\272", nullptr));
        option_check_3->setText(QCoreApplication::translate("MainWindow", "\351\241\257\347\244\272\344\272\214\351\232\216\350\231\225\347\220\206\351\201\216\347\250\213", nullptr));
        groupBox_4->setTitle(QCoreApplication::translate("MainWindow", "\345\237\272\346\234\254\350\263\207\350\250\212", nullptr));
        image_w->setText(QCoreApplication::translate("MainWindow", "Width", nullptr));
        image_h->setText(QCoreApplication::translate("MainWindow", "Height", nullptr));
        image_c->setText(QCoreApplication::translate("MainWindow", "Channel", nullptr));
        image_h_val->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        image_c_val->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        image_w_val->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        label_3->setText(QCoreApplication::translate("MainWindow", "\351\201\213\347\256\227\346\231\202\351\226\223", nullptr));
        label_time->setText(QCoreApplication::translate("MainWindow", "-", nullptr));
        label_7->setText(QCoreApplication::translate("MainWindow", "sec", nullptr));
    } // retranslateUi

};

namespace Ui {
    class MainWindow: public Ui_MainWindow {};
} // namespace Ui

QT_END_NAMESPACE

#endif // UI_MAINWINDOW_H
