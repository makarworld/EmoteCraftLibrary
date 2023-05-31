# coding:utf-8
import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPixmap, QIcon, QMovie, QCursor
from PyQt5.QtWidgets import QApplication, QLabel

from qframelesswindow import FramelessWindow, StandardTitleBar


class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)

        # customize the style of title bar button
        self.minBtn.setHoverColor(Qt.white)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.white)
        self.minBtn.setPressedBackgroundColor(QColor(54, 57, 65))

        # use qss to customize title bar button
        self.maxBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-hoverColor: white;
                qproperty-hoverBackgroundColor: rgb(0, 100, 182);
                qproperty-pressedColor: white;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)


class Window(FramelessWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # change the default title bar if you like
        self.setTitleBar(CustomTitleBar(self))
        self.setFixedSize(256, 256)
        mouse = QCursor.pos()
        self.setGeometry(mouse.x(), mouse.y(), 256, 256)
        
        #always ob top
        self.setWindowFlag(Qt.WindowStaysOnTopHint, True)
        self.setWindowFlag(Qt.FramelessWindowHint, True)

        #self.label = QLabel(self)
        #self.label.setScaledContents(True)
        #self.label.setPixmap(QPixmap("screenshot/shoko.png"))
        if len(sys.argv) < 2:
            file_path = "./src/textures/zombie 3.gif"
            #exit(1)
        else:
            file_path = sys.argv[1] #"./src/textures/zombie 3.gif"

        self.label = QLabel(self)
        self.label.setScaledContents(True)
        self.movie = QMovie(file_path)
        self.movie.setSpeed(150)
        self.label.setMovie(self.movie)
        self.movie.start()

        self.setWindowIcon(QIcon(file_path))
        self.setWindowTitle(os.path.basename(file_path))
        self.setStyleSheet("background:white")

        self.titleBar.raise_()

    def resizeEvent(self, e):
        # don't forget to call the resizeEvent() of super class
        super().resizeEvent(e)
        length = min(self.width(), self.height())
        self.label.resize(length, length)
        self.label.move(
            self.width() // 2 - length // 2,
            self.height() // 2 - length // 2
        )


if __name__ == "__main__":
    # enable dpi scale
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    
    # run app
    app = QApplication(sys.argv)
    demo = Window()
    demo.show()
    sys.exit(app.exec_())