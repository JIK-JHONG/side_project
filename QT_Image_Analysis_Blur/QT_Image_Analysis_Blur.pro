QT       += core gui

greaterThan(QT_MAJOR_VERSION, 4): QT += widgets

CONFIG += c++11

# You can make your code fail to compile if it uses deprecated APIs.
# In order to do so, uncomment the following line.
#DEFINES += QT_DISABLE_DEPRECATED_BEFORE=0x060000    # disables all the APIs deprecated before Qt 6.0.0

SOURCES += \
    image_process.cpp \
    main.cpp \
    mainwindow.cpp

HEADERS += \
    image_process.h \
    mainwindow.h

FORMS += \
    mainwindow.ui

TRANSLATIONS += \
    QT_Image_Analysis_Blur_zh_TW.ts
CONFIG += lrelease
CONFIG += embed_translations

# OpenCV 路徑設置
INCLUDEPATH += /opt/homebrew/opt/opencv@4/include/opencv4
LIBS += -L/opt/homebrew/opt/opencv@4/lib -lopencv_core -lopencv_imgcodecs -lopencv_highgui -lopencv_imgproc

# Default rules for deployment.
qnx: target.path = /tmp/$${TARGET}/bin
else: unix:!android: target.path = /opt/$${TARGET}/bin
!isEmpty(target.path): INSTALLS += target

RESOURCES += \
    resource.qrc
