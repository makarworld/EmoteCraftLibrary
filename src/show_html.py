# coding: utf-8

import os
import sys
import websocket
from threading import Thread
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QOpenGLWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView


from _qframelesswindow import FramelessMainWindow, StandardTitleBar


class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)

        # customize the style of title bar button
        self.minBtn.setHoverColor(Qt.black)
        self.minBtn.setHoverBackgroundColor(QColor(0, 100, 182))
        self.minBtn.setPressedColor(Qt.black)
        self.minBtn.setPressedBackgroundColor(QColor(54, 57, 65))

        # use qss to customize title bar button
        self.maxBtn.setStyleSheet("""
            TitleBarButton {
                qproperty-hoverColor: black;
                qproperty-hoverBackgroundColor: rgb(0, 100, 182);
                qproperty-pressedColor: black;
                qproperty-pressedBackgroundColor: rgb(54, 57, 65);
            }
        """)




class MainWindow(FramelessMainWindow):
    def __init__(self):
        super().__init__()
        self.setTitleBar(CustomTitleBar(self))

        # Set window properties
        #self.setWindowTitle("Web Page")
        self.setGeometry(100, 100, 1280, 688)

        

        # Create web view widget
        self.web_view = QWebEngineView()

        html_path = os.path.split(os.path.abspath(__file__))[0] + r'\ui\index.html'
        self.web_view.load(QUrl().fromLocalFile(
            html_path
        )) #

        self.web_view.setContentsMargins(0, 0, 0, 0)
        #self.web_view.setSizeAdjustPolicy(QWebEngineView.AdjustSizeOnResize)
        self.web_view.setUpdatesEnabled(True)
        self.web_view

        self.setWindowFlags(Qt.FramelessWindowHint)

        # Set central widget
        self.setCentralWidget(self.web_view)
        #self.showFullScreen()
        self.titleBar.raise_()


#QApplication.setHighDpiScaleFactorRoundingPolicy(
#    Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
#QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
#QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)




# create window
qtapp = QApplication(sys.argv)
window = MainWindow()
window.show()

#t = Thread(target=lambda: app.run(host='127.0.0.1', port='2222'))
#t.start()

#t = Thread(target=lambda: qtapp.exec_())
#t.start()
from loguru import logger 

try:
    print(qtapp.exec_())
except Exception as e:
    logger.exception(e)

    sys.exit()


## host http server for receive commands
#t = Thread(target=lambda: app.run(host='127.0.0.1', port='2222'))
#t.daemon = True
#t.start()
#app.run(host='127.0.0.1', port='2222')
#while