#from PySide6.QtWidgets import QApplication, QWidget, QLabel
#from PySide6.QtGui import QIcon, QMovie
#import sys 
#from PySide6 import QtCore, QtGui
#from qframelesswindow import FramelessWindow
#
#class Window(FramelessWindow):
#    def __init__(self):
#        super().__init__()
#        self.label = QLabel(self)
#        self.movie = QMovie("./src/textures/zombie 3.gif")
#        self.label.setMovie(self.movie)
#        self.movie.start()
#        self.setCentralWidget(self.label)
#        self.setStyleSheet("QTextEdit {border: 1px solid black;}")
#        #self.setWindowIcon(QIcon("icon.png"))
#        #self.setGeometry(100, 100, 256, 256)
#        self.setMaximumHeight(240)
#
#
#app = QApplication(sys.argv)
#window = Window()
#window.show()
#sys.exit(app.exec())

import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=800, height=600)

demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
