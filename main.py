from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QDialog, QMainWindow, QTabWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QSpacerItem, QStatusBar, QToolBar, QAction, QLineEdit
from PyQt5.QtWebEngineWidgets import QWebEngineView
import sys
from modules.user_data import Settings, ensure_user_data_exists

ensure_user_data_exists()
DEFAULT_PAGE = Settings.get("default_page","https://duckduckgo.com/")
USER_AGENT = Settings.get("user_agent","Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) QtWebEngine/5.15.2 Chrome/83.0.4103.122 Safari/537.36")

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.title = 'PyQt5 Webbrowser - Settings'
        self.setWindowTitle(self.title)
        self.initUI()
 
    def initUI(self):
        layout = QVBoxLayout()
        
        self.adjustSize()
        
        self.start_page_text = QLabel("Startpage", self)
        layout.addWidget(self.start_page_text)
        
        # Default page QLineEdit
        self.default_page_textbox = QLineEdit(self)
        self.default_page_textbox.setText(DEFAULT_PAGE)
        layout.addWidget(self.default_page_textbox)
        
        self.user_agent_text = QLabel("User Agent", self)
        layout.addWidget(self.user_agent_text)
        
        # User agent QLineEdit
        self.user_agent_textbox = QLineEdit(self)
        self.user_agent_textbox.setText(USER_AGENT)
        layout.addWidget(self.user_agent_textbox)
        
        # Warning text
        self.warning_text = QLabel("Changes only take effect after restarting", self)
        layout.addWidget(self.warning_text)
        
        # Save button
        save_button = QPushButton("Save Changes")
        save_button.clicked.connect(self.save_changes)
        layout.addWidget(save_button)
        
        # Set the layout
        self.setLayout(layout)

    def save_changes(self):
        # Save the new default page setting
        Settings.set("default_page", self.default_page_textbox.text())
        Settings.set("user_agent", self.user_agent_textbox.text())

        # Optionally, adjust the size of the dialog to fit the content
        self.adjustSize()

class MainWindow(QMainWindow):
    """
    Main application window for the PyQt5 web browser.

    This class sets up the main window, navigation toolbar, and manages tabs and URLs.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the MainWindow with a set of default properties and layouts.

        Parameters
        ----------
        *args : tuple
            Variable length argument list passed to the parent constructor.
        **kwargs : dict
            Arbitrary keyword arguments passed to the parent constructor.
        """
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
        self.add_new_tab(QUrl(DEFAULT_PAGE), 'Homepage')
        self.setWindowTitle("PyQT5 Webbrowser")
        self.show()

    def setup_navigation_toolbar(self):
        """
        Set up the navigation toolbar with common web browsing actions.

        This includes buttons for going back, forward, reloading, going home, and stopping the page load.
        """
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
        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings_dialog)
        navtb.addAction(settings_action)
    
    def open_settings_dialog(self):
        settings_dialog = SettingsDialog(self)
        if settings_dialog.exec_() == QDialog.Accepted:
            pass

    def add_new_tab(self, qurl=None, label="Blank"):
        """
        Add a new tab to the tab widget with the specified URL and label.

        Parameters
        ----------
        qurl : QUrl, optional
            The URL to load in the new tab, by default None which loads the homepage.
        label : str, optional
            The label for the new tab, by default 'Blank'.
        """
        
        if qurl is None:
            qurl = QUrl(DEFAULT_PAGE)
        browser = QWebEngineView()

        #set custom user agent
        profile = browser.page().profile()
        profile.setHttpUserAgent(USER_AGENT)

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
        self.tabs.currentWidget().setUrl(QUrl(DEFAULT_PAGE))

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
