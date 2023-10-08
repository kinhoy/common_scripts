import sys
import os
import math
import cv2
from PyQt5.QtCore import Qt  # 导入Qt模块
from PyQt5.QtWidgets import QMessageBox, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QSlider, QPushButton, QFileDialog
from PyQt5.QtGui import QPixmap, QImage, QPainter, QTransform, QPen
class ImageRotateTool(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # mini_size 窗口缩小比例
        self.mini_size = 9
        self.originalImage = None
        self.currentImage = None
        self.cv_img = None
        self.cv_dst_img = None

        self.directory_path = ''
        self.file_name = ''
        self.angle = 0

        mainLayout = QVBoxLayout()

        self.imageLabel = QLabel(self)
        mainLayout.addWidget(self.imageLabel)

        buttonLayout = QHBoxLayout()

        self.loadButton = QPushButton("加载图片")
        self.loadButton.clicked.connect(self.loadImage)
        buttonLayout.addWidget(self.loadButton)

        # 创建一个按钮，用于选择目录
        self.selectDirectoryButton = QPushButton("选择导出目录")
        self.selectDirectoryButton.clicked.connect(self.selectDirectory)
        buttonLayout.addWidget(self.selectDirectoryButton)

        self.saveButton = QPushButton("保存图片")
        self.saveButton.clicked.connect(self.saveImage)
        buttonLayout.addWidget(self.saveButton)

        mainLayout.addLayout(buttonLayout)

        self.angleSlider = QSlider(Qt.Horizontal)  # 粗调整-整数角度部分
        self.angleSlider.setMinimum(-180)
        self.angleSlider.setMaximum(180)
        self.angleSlider.setValue(0)
        self.angleSlider.valueChanged.connect(self.rotateImage)
        mainLayout.addWidget(self.angleSlider)

        self.mini_angleSlider = QSlider(Qt.Horizontal)  # 细调整-小数角度部分
        self.mini_angleSlider.setMinimum(-99)
        self.mini_angleSlider.setMaximum(99)
        self.mini_angleSlider.setValue(0)
        self.mini_angleSlider.valueChanged.connect(self.rotateImage)
        mainLayout.addWidget(self.mini_angleSlider)

        self.setLayout(mainLayout)
        self.setWindowTitle("图片旋转工具")
    
    def selectDirectory(self):
        # 弹出目录选择对话框
        self.directory_path = QFileDialog.getExistingDirectory(self, "选择目标目录")

    def drawMask(self):
        if self.currentImage:
            # 创建一个QPainter对象，用于在当前图像上绘制遮罩
            painter = QPainter(self.currentImage)
            painter.setRenderHint(QPainter.Antialiasing)

            # 定义水平线和垂直线的颜色和宽度
            line_color = Qt.red  # 您可以根据需要选择颜色
            line_width = 8

            # 绘制水平线
            for i in range(1, 8):
                y = i * self.originalImage.height() // 8
                painter.setPen(QPen(line_color, line_width))
                painter.drawLine(0, y, self.originalImage.width(), y)

            # 绘制垂直线
            for i in range(1, 8):
                x = i * self.originalImage.width() // 8
                painter.setPen(QPen(line_color, line_width))
                painter.drawLine(x, 0, x, self.originalImage.height())

            # 结束绘制
            painter.end()

            # 更新标签上的图像
            self.updateImageLabel()
        
    def loadImage(self):
        filePath, _ = QFileDialog.getOpenFileName(self, "选择图片文件", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
        if filePath:
            self.file_name = os.path.basename(filePath)
            self.originalImage = QImage(filePath)
            self.currentImage = self.originalImage.copy()
            self.angle = 0
            self.angleSlider.setValue(0)
            self.mini_angleSlider.setValue(0)
            # 绘制遮罩
            self.drawMask()

            self.updateImageLabel()
            
            self.cv_img = cv2.imread(filePath, cv2.IMREAD_GRAYSCALE)

            self.setFixedSize(int(1.2*self.originalImage.width()// self.mini_size), int(1.2*self.originalImage.height()// self.mini_size))

            img_name = filePath.split('/')[-1]  # 获取文件名部分
            self.setWindowTitle(f'正在操作图片 - {img_name}')

    def rotateImage(self):
        self.angle = self.angleSlider.value() + self.mini_angleSlider.value() / 100 
        print("旋转角度为："+str(self.angle))
        transform = QTransform()
        transform.rotate(self.angle)
        self.currentImage = self.originalImage.transformed(transform)

        center = (self.cv_img.shape[1] // 2, self.cv_img.shape[0] // 2)
        rotMat = cv2.getRotationMatrix2D(center, -1 * self.angle, 1.0)
        # 用白色填充图片周围
        self.cv_dst_img = cv2.warpAffine(self.cv_img, rotMat, self.cv_img.shape[::-1], borderValue=255)

        # 绘制遮罩
        self.drawMask()

        self.updateImageLabel()

    def saveImage(self):
        if self.currentImage:
            # filePath, _ = QFileDialog.getSaveFileName(self, "保存图片文件", "", "Images (*.png *.jpg *.jpeg *.bmp *.gif)")
            # if filePath:
            #     # self.currentImage.save(filePath)
            #     cv2.imwrite(filePath, self.cv_dst_img)
            #     print(filePath)
            if self.directory_path:
                output_path = os.path.join(self.directory_path, self.file_name)
                cv2.imwrite(output_path, self.cv_dst_img)
                QMessageBox.information(self,"操作成功","图片已保存", QMessageBox.Yes)
                print(output_path)
            else:
                print("请选择图片保存路径")
                QMessageBox.information(self,"注意","请选择图片保存路径", QMessageBox.Yes)

    def updateImageLabel(self):
        if self.currentImage:
            scaled_image = self.currentImage.scaledToWidth(self.currentImage.width() // self.mini_size)
            pixmap = QPixmap.fromImage(scaled_image)
            self.imageLabel.setPixmap(pixmap)

def main():
    app = QApplication(sys.argv)
    tool = ImageRotateTool()
    tool.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
