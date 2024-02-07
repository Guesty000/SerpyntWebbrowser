import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtWebEngineWidgets import *

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.tabBarDoubleClicked.connect(self.tab_open_doubleclick)
        self.tabs.currentChanged.connect(self.current_tab_changed)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_current_tab)
        self.setCentralWidget(self.tabs)
        self.status = QStatusBar()
        self.setStatusBar(self.status)
        self.setup_navigation_toolbar()
        self.add_new_tab(QUrl('http://www.google.com'), 'Homepage')
        self.setWindowTitle("PyQT5 Webbrowser")
        self.show()

    def setup_navigation_toolbar(self):
        navtb = QToolBar("Navigation")
        self.addToolBar(navtb)
        actions = [
            ("Back", "Back to previous page", self.back_action),
            ("Forward", "Forward to next page", self.forward_action),
            ("Reload", "Reload page", self.reload_action),
            ("Home", "Go home", self.navigate_home),
            ("Stop", "Stop loading current page", self.stop_action)
        ]
        for name, status_tip, function in actions:
            button = QAction(name, self)
            button.setStatusTip(status_tip)
            button.triggered.connect(function)
            navtb.addAction(button)
        navtb.addSeparator()
        self.urlbar = QLineEdit()
        self.urlbar.returnPressed.connect(self.navigate_to_url)
        navtb.addWidget(self.urlbar)

    def add_new_tab(self, qurl=None, label="Blank"):
        if qurl is None:
            qurl = QUrl('http://www.google.com')
        browser = QWebEngineView()
        browser.setUrl(qurl)
        i = self.tabs.addTab(browser, label)
        self.tabs.setCurrentIndex(i)
        browser.urlChanged.connect(lambda qurl, browser=browser: self.update_urlbar(qurl, browser))
        browser.loadFinished.connect(lambda _, i=i, browser=browser: self.tabs.setTabText(i, browser.page().title()))

    def tab_open_doubleclick(self, i):
        if i == -1:
            self.add_new_tab()

    def current_tab_changed(self, i):
        qurl = self.tabs.currentWidget().url()
        self.update_urlbar(qurl, self.tabs.currentWidget())
        self.update_title(self.tabs.currentWidget())

    def close_current_tab(self, i):
        if self.tabs.count() < 2:
            return
        self.tabs.removeTab(i)

    def update_title(self, browser):
        if browser != self.tabs.currentWidget():
            return
        title = self.tabs.currentWidget().page().title()
        self.setWindowTitle("% s - PyQT5 Webbrowser" % title)

    def navigate_home(self):
        self.tabs.currentWidget().setUrl(QUrl("http://www.google.com"))

    def navigate_to_url(self):
        q = QUrl(self.urlbar.text())
        if q.scheme() == "":
            q.setScheme("http")
        self.tabs.currentWidget().setUrl(q)

    def update_urlbar(self, q, browser=None):
        if browser != self.tabs.currentWidget():
            return
        self.urlbar.setText(q.toString())
        self.urlbar.setCursorPosition(0)

    def back_action(self):
        current_widget = self.tabs.currentWidget()
        if current_widget:
            current_widget.back()

    def forward_action(self):
        current_widget = self.tabs.currentWidget()
        if current_widget:
            current_widget.forward()

    def reload_action(self):
        current_widget = self.tabs.currentWidget()
        if current_widget:
            current_widget.reload()

    def stop_action(self):
        current_widget = self.tabs.currentWidget()
        if current_widget:
            current_widget.stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec_()
