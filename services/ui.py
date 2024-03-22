import random
import sys
import os

from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QFrame
from PySide6.QtGui import QPixmap, QFont
from PySide6.QtCore import Qt, QTimer

# import server
from services.server import get_data


class ImageViewer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 主布局分为两列
        mainLayout = QHBoxLayout()

        # 左列布局用于显示图片和数据
        leftLayout = QVBoxLayout()

        leftTitleLabel = QLabel("Object and Action Detection")
        leftTitleLabel.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 16, QFont.Bold)
        leftTitleLabel.setFont(title_font)
        # 创建水平布局用于放置左侧的标题和图片
        leftTitleLayout = QHBoxLayout()
        leftTitleLayout.addWidget(leftTitleLabel)

        self.imageLabel1 = QLabel()
        self.imageLabel1.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        leftLayout.addLayout(leftTitleLayout)
        leftLayout.addWidget(self.imageLabel1)

        # 创建一个容器来围绕四个数据标签
        dataContainer1 = QFrame()
        dataContainer1.setObjectName("dataContainer")
        dataContainer1Layout = QVBoxLayout()
        leftLayout.addWidget(dataContainer1)

        # 创建四个数据标签
        self.dataLabels1 = [QLabel(f"Data {i+1}: [Value]") for i in range(4)]
        for label in self.dataLabels1:
            dataContainer1Layout.addWidget(label)

        dataContainer1.setLayout(dataContainer1Layout)

        # 右列布局
        rightLayout = QVBoxLayout()

        rightTitleLabel = QLabel("Gesture Detection")
        rightTitleLabel.setAlignment(Qt.AlignCenter)
        title_font = QFont("Arial", 16, QFont.Bold)
        rightTitleLabel.setFont(title_font)
        # 创建水平布局用于放置右侧的标题
        rightTitleLayout = QHBoxLayout()
        rightTitleLayout.addWidget(rightTitleLabel)

        self.imageLabel2 = QLabel()
        self.imageLabel2.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        rightLayout.addLayout(rightTitleLayout)
        rightLayout.addWidget(self.imageLabel2)

        # 创建一个容器来围绕右侧两个数据标签
        dataContainer2 = QFrame()
        dataContainer2.setObjectName("dataContainer")
        dataContainer2Layout = QVBoxLayout()
        rightLayout.addWidget(dataContainer2)

        self.gestureLabel = QLabel("Gesture Name: 92.8")
        self.accuracyLabel = QLabel("Accuracy: 99.3")
        dataContainer2Layout.addWidget(self.gestureLabel)
        dataContainer2Layout.addWidget(self.accuracyLabel)

        dataContainer2.setLayout(dataContainer2Layout)

        # 将两列布局添加到主布局
        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rightLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Human Robot Interactions System")
        self.setGeometry(100, 100, 800, 600)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_data)
        self.timer.start(1000)  # 1秒钟更新一次数据

        # 应用样式表
        self.setStyleSheet("""
            #dataContainer {
                background-color: #f0f0f0;
                border: 1px solid black; /* 添加黑色边框 */
                border-radius: 10px;
                padding: 10px;
                margin-bottom: 10px;
                box-shadow: 5px 5px 5px rgba(0, 0, 0, 0.5); /* 添加阴影效果 */
            }
        """)

    def update_data(self):
        data = get_data()
        print(data)
        for i, (key, value) in enumerate(data.items()):
            if i < len(self.dataLabels1):
                self.dataLabels1[i].setText(f"{key}: {value}")

        # 从images文件夹中取一张固定图片
        images_folder = 'images'
        images = [img for img in os.listdir(images_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if images:
            self.imageLabel1.setPixmap(QPixmap(os.path.join(images_folder, images[0])).scaled(400, 300, Qt.KeepAspectRatio))

        # 从resources文件夹中随机选择一张图片
        resource_folder = 'resources'
        images = [img for img in os.listdir(resource_folder) if img.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
        if images:
            random_image_path = random.choice(images)
            self.imageLabel2.setPixmap(QPixmap(os.path.join(resource_folder, random_image_path)).scaled(400, 300, Qt.KeepAspectRatio))

        # 生成两个随机数字，用于更新右侧布局中的标签内容
        random_numbers = round(random.uniform(90, 100), 1)
        self.gestureLabel.setText(f"Gesture Name: {random_numbers + 2}")
        self.accuracyLabel.setText(f"Accuracy: {random_numbers - 3}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ImageViewer()
    ex.show()
    sys.exit(app.exec())
