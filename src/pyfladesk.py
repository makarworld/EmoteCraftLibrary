# thanks
# https://github.com/smoqadam/PyFladesk/blob/master/pyfladesk/__init__.py
#
import sys
from PyQt5 import QtCore, QtWidgets, QtGui, QtWebEngineWidgets
import socket

from _qframelesswindow import FramelessMainWindow, StandardTitleBar

class CustomTitleBar(StandardTitleBar):
    """ Custom title bar """

    def __init__(self, parent):
        super().__init__(parent)

        # customize the style of title bar button
        self.minBtn.setHoverColor(QtCore.Qt.black)
        self.minBtn.setHoverBackgroundColor(QtGui.QColor(0, 100, 182))
        self.minBtn.setPressedColor(QtCore.Qt.black)
        self.minBtn.setPressedBackgroundColor(QtGui.QColor(54, 57, 65))

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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

class ApplicationThread(QtCore.QThread):
    def __init__(self, application, port=5000):
        super(ApplicationThread, self).__init__()
        self.application = application
        self.port = port

    def __del__(self):
        self.wait()

    def run(self):
        self.application.run(port=self.port, threaded=True)


class WebPage(QtWebEngineWidgets.QWebEnginePage):
    def __init__(self, root_url):
        super(WebPage, self).__init__()
        self.root_url = root_url

    def home(self):
        self.load(QtCore.QUrl(self.root_url))

    def acceptNavigationRequest(self, url, kind, is_main_frame):
        """Open external links in browser and internal links in the webview"""
        ready_url = url.toEncoded().data().decode()
        is_clicked = kind == self.NavigationTypeLinkClicked
        if is_clicked and self.root_url not in ready_url:
            QtGui.QDesktopServices.openUrl(url)
            return False
        return super(WebPage, self).acceptNavigationRequest(url, kind, is_main_frame)


def init_gui(application, port=0, width=800, height=600, argv=None):
    if argv is None:
        argv = sys.argv

    if port == 0:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind(('localhost', 0))
        port = sock.getsockname()[1]
        sock.close()

    # Application Level
    qtapp = QtWidgets.QApplication(argv)
    webapp = ApplicationThread(application, port)
    webapp.start()
    qtapp.aboutToQuit.connect(webapp.terminate)

    # Main Window Level
    window = MainWindow()
    window.resize(width, height)

    # WebView Level
    webView = QtWebEngineWidgets.QWebEngineView(window)
    webView.setContentsMargins(0, 0, 0, 0)
    webView.setUpdatesEnabled(True)
    window.setCentralWidget(webView)

    # WebPage Level
    page = WebPage('http://localhost:{}'.format(port))
    page.home()
    webView.setPage(page)

    window.titleBar.raise_()
    window.show()
    return qtapp.exec_()