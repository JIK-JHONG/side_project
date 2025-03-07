import sys
import cv2
import numpy as np
import Image_Processing as ip # 引入副程式中的函式
print(dir(ip))  # 列出 Image_Processing 模組中的所有屬性

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap, QImage, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QApplication, QWidget, QGraphicsScene, QGraphicsPixmapItem, QFileDialog, QHeaderView, QLabel
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from ui_form import Ui_Widget  # 自動生成的 UI 介面
import time


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.setWindowTitle("Image Process")

        # 建立 QGraphicsScene 來顯示圖片
        # 創建不同的場景
        self.scene1 = QGraphicsScene()
        self.scene2 = QGraphicsScene()
        self.scene3 = QGraphicsScene()

        # 為每個視圖設置不同的場景
        self.ui.graphicsView.setScene(self.scene1)
        self.ui.graphicsView_2.setScene(self.scene2)
        self.ui.graphicsView_3.setScene(self.scene3)

        # 設定 tableView 的 model
        self.model = QStandardItemModel(3, 2)  # 3 行 2 列
        self.model.setHorizontalHeaderLabels(["屬性", "數值"])
        self.ui.tableView.setModel(self.model)



        # **調整 tableView 的大小行為**
        self.ui.tableView.horizontalHeader().setStretchLastSection(True)  # 讓最後一欄填滿
        self.ui.tableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)  # 調整第一欄
        self.ui.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)  # 調整第二欄
        self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)  # 行高填滿

        # **關閉捲動條**
        self.ui.tableView.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 關閉垂直捲動條
        self.ui.tableView.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 關閉水平捲動條


        self.ui.label_5.setText(str(80))
        self.ui.label_7.setText(str(0))
        self.ui.label_9.setText(str(5))

        self.ui.label_process_time.setText("-")

        self.ui.horizontalSlider.setMinimum(0)
        self.ui.horizontalSlider.setMaximum(255)
        self.ui.horizontalSlider.setValue(80)

        self.ui.horizontalSlider_2.setMinimum(0)
        self.ui.horizontalSlider_2.setMaximum(200)
        self.ui.horizontalSlider_2.setValue(5)

        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setValue(0)
        # 綁定 pushButton 事件
        self.ui.pushButton.clicked.connect(self.load_image)
        print(sys.path)

        self.ui.horizontalSlider.valueChanged.connect(self.onChangeHorizontalSlider)
        self.ui.horizontalSlider_2.valueChanged.connect(self.onChangeHorizontalSlider_2)


        self.img_input_buffer = None

        print(dir(self.ui))  # 列出 self.ui 內所有物件

    def load_image(self):
        """選擇圖片並顯示在 graphicsView"""
        total_counter= 0
        self.ui.label_7.setText(str(total_counter))
        file_path, _ = QFileDialog.getOpenFileName(self, "選擇圖片", "", "Images (*.png *.jpg *.bmp *.jpeg)")

        if file_path:
            # 在 lineEdit 顯示圖片路徑
            self.ui.lineEdit.setText(file_path)

            # 使用 OpenCV 讀取圖片
            img = cv2.imread(file_path)

            if img is None:
                print("無法讀取圖片")
                return

            # **轉換 BGR → RGB**
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            self.img_input_buffer = img.copy()
            self.update_image_profile(img)

            # 取得圖片資訊
            height, width, channel = img.shape  # (高度, 寬度, 通道數)
            if (channel == 3):
                img_type = "RGB"
            elif (channel == 4):
                img_type = "RGBA"
            elif (channel == 1):
                img_type = "GRAY"
            else:
                img_type = "Unknown"


            # 轉換為 QImage
            bytes_per_line = channel * width
            q_image = QImage(img.data, width, height, bytes_per_line, QImage.Format_RGB888)

            # 轉換為 QPixmap 以顯示
            pixmap = QPixmap.fromImage(q_image)

            # 清除之前的內容
            self.scene1.clear()

            # 創建 QGraphicsPixmapItem 來顯示圖片
            pixmap_item = QGraphicsPixmapItem(pixmap)
            self.scene1.addItem(pixmap_item)

            # 讓 scene1 大小匹配圖片
            self.scene1.setSceneRect(pixmap.rect())

            # 等比縮放圖片至 graphicsView
            self.ui.graphicsView.fitInView(self.scene1.sceneRect(), Qt.KeepAspectRatio)

            # 更新 tableView 內容
            self.update_table([
                ("Width", width),
                ("Height", height),
                ("Type", img_type)
            ])


            self.ImageView(img)
            self.ui.progressBar.setValue(100)

    def update_table(self, data):
        """更新 tableView 內容"""
        self.model.removeRows(0, self.model.rowCount())  # 清除舊資料
        for row, (key, value) in enumerate(data):
            self.model.setItem(row, 0, QStandardItem(str(key)))
            self.model.setItem(row, 1, QStandardItem(str(value)))


    def update_timer_in_process(self,finished_time):
        # print(f">>>>>finished time = {finished_time}")
        self.ui.label_process_time.setText(str(finished_time))


    def ImageView(self, img):
        start_time = time.time()
        self.ui.progressBar.setValue(0)
        # fig = ip.ImageBinary(img,'normal')
        fig , total_counter = ip.object_detected(img,self.getHorizontalSlider(),self.getHorizontalSlider_2())

        height, width, channel = fig.shape  # (高度, 寬度, 通道數)
        # 轉換為 QImage
        bytes_per_line = channel * width
        q_image = QImage(fig.data, width, height, bytes_per_line, QImage.Format_RGB888)

        # 將 QImage 轉換為 QPixmap
        pixmap = QPixmap.fromImage(q_image)

        # 清空並重新添加新的圖形
        self.scene2.clear()  # 清空現有場景中的項目
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene2.addItem(pixmap_item)

        # 設定場景範圍以適應圖形
        self.scene2.setSceneRect(pixmap_item.boundingRect())  # 更新場景的邊界範圍

        # 使用 graphicsView3 進行更新，確保圖片適應視窗
        self.ui.graphicsView_2.fitInView(self.scene2.sceneRect(), Qt.KeepAspectRatio)
        self.ui.graphicsView_2.setSceneRect(self.scene2.sceneRect())


        self.ui.label_7.setText(str(total_counter))
        self.ui.progressBar.setValue(100)

        end_time = time.time()
        elapsed_time = round(end_time - start_time, 2)
        self.update_timer_in_process(elapsed_time)


    def update_image_profile(self, img):
        # 假設 image_analysis() 會返回 Matplotlib 的畫布 (FigureCanvas)
        fig = ip.image_analysis(img,"x")
        canvas = FigureCanvas(fig)
        canvas.draw()

        # 將 matplotlib 的畫布轉換為 QImage
        width, height = canvas.get_width_height()
        print(f"width= {width}, height = {height}")
        image = canvas.buffer_rgba()

        # Convert memoryview to QImage
        qimage = QImage(image, width, height, QImage.Format_RGBA8888)

        # 將 QImage 轉換為 QPixmap
        pixmap = QPixmap.fromImage(qimage)

        # 清空並重新添加新的圖形
        self.scene3.clear()  # 清空現有場景中的項目
        pixmap_item = QGraphicsPixmapItem(pixmap)
        self.scene3.addItem(pixmap_item)

        # 設定場景範圍以適應圖形
        self.scene3.setSceneRect(pixmap_item.boundingRect())  # 更新場景的邊界範圍

        # 使用 graphicsView3 進行更新，確保圖片適應視窗
        self.ui.graphicsView_3.fitInView(self.scene3.sceneRect(), Qt.KeepAspectRatio)
        self.ui.graphicsView_3.setSceneRect(self.scene3.sceneRect())

    def onChangeHorizontalSlider(self):
        val = self.ui.horizontalSlider.value()
        self.ui.label_5.setText(str(val))
        self.ImageView(self.img_input_buffer)



    def getHorizontalSlider(self):
        val = self.ui.horizontalSlider.value()
        return val

    def onChangeHorizontalSlider_2(self):
        val = self.ui.horizontalSlider_2.value()
        if val % 2 == 0:
                # 如果是偶數，將其加1以變成奇數
                val += 1
        self.ui.label_9.setText(str(val))
        self.ui.horizontalSlider_2.setValue(val)
        self.ImageView(self.img_input_buffer)



    def getHorizontalSlider_2(self):
        val = self.ui.horizontalSlider_2.value()
        return val


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec())
