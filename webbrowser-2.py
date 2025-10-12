import sys
import os
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtGui import QIcon
import os

# Set Window Icon and Title



from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QVBoxLayout, QWidget,
    QAction, QLineEdit, QToolBar, QFileDialog, QMessageBox
)
from PyQt5.QtWebEngineWidgets import (
    QWebEngineView, QWebEngineProfile, QWebEnginePage, QWebEngineDownloadItem
)


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        icon_path = os.path.join(os.path.dirname(__file__), "brand-logo.jpg")
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle("Deepjyoti Browser 🌐")
        self.resize(1200, 800)

        # Default profile
        self.default_profile = QWebEngineProfile.defaultProfile()
        self.default_profile.settings().setAttribute(
            self.default_profile.settings().PluginsEnabled, False
        )

        # Simple adblock script placeholder
        self.adblock_script = self.default_profile.scripts()

        # Tabs setup
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.setCentralWidget(self.tabs)

        # Toolbar setup
        nav_bar = QToolBar("Navigation")
        self.addToolBar(nav_bar)

        # Buttons
        back_btn = QAction("⬅️", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        nav_bar.addAction(back_btn)

        forward_btn = QAction("➡️", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        nav_bar.addAction(forward_btn)

        reload_btn = QAction("🔄", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        nav_bar.addAction(reload_btn)

        home_btn = QAction("🏠", self)
        home_btn.triggered.connect(self.navigate_home)
        nav_bar.addAction(home_btn)

        incognito_btn = QAction("🕶️ Incognito", self)
        incognito_btn.triggered.connect(self.open_incognito_tab)
        nav_bar.addAction(incognito_btn)

        new_tab_btn = QAction("➕ New Tab", self)
        new_tab_btn.triggered.connect(lambda: self.add_tab(incognito=False))
        nav_bar.addAction(new_tab_btn)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        nav_bar.addWidget(self.url_bar)

        # Add initial tab
        self.add_tab(incognito=False, url=QUrl("https://www.google.com"))

    # ---------------------------------------------------------------------
    def add_tab(self, incognito=False, url=QUrl("https://www.google.com")):
        """Add a new tab."""
        if incognito:
            profile = QWebEngineProfile()
            profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
            profile.setCachePath("")
            profile.setPersistentStoragePath("")
        else:
            profile = self.default_profile

        webview = QWebEngineView()
        webview.setPage(QWebEnginePage(profile, webview))
        webview.setUrl(url)

        # Signals
        webview.urlChanged.connect(self.update_url)
        webview.titleChanged.connect(lambda title: self.tabs.setTabText(self.tabs.indexOf(tab), title))
        webview.loadFinished.connect(self.add_history)
        webview.page().profile().downloadRequested.connect(self.download_file)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(webview)

        tab = QWidget()
        tab.setLayout(layout)
        index = self.tabs.addTab(tab, "New Tab (Incognito)" if incognito else "New Tab")
        self.tabs.setCurrentIndex(index)

    # ---------------------------------------------------------------------
    def current_browser(self):
        """Return current QWebEngineView."""
        current_tab = self.tabs.currentWidget()
        if current_tab:
            return current_tab.layout().itemAt(0).widget()
        return None

    def navigate_home(self):
        browser = self.current_browser()
        if browser:
            browser.setUrl(QUrl("https://www.google.com"))

    def navigate_to_url(self):
        url_text = self.url_bar.text()
        if not url_text.startswith("http"):
            url_text = "https://" + url_text
        self.current_browser().setUrl(QUrl(url_text))

    def update_url(self, url):
        self.url_bar.setText(url.toString())

    def add_history(self):
        browser = self.current_browser()
        if browser:
            print(f"Visited: {browser.url().toString()}")

    def open_incognito_tab(self):
        self.add_tab(incognito=True, url=QUrl("https://www.google.com"))

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            QMessageBox.information(self, "Notice", "Cannot close the last tab.")

    # ---------------------------------------------------------------------
    def download_file(self, download: QWebEngineDownloadItem):
        """Handle file downloads."""
        suggested_name = download.downloadFileName()
        path, _ = QFileDialog.getSaveFileName(self, "Save File As", suggested_name)
        if path:
            download.setPath(path)
            download.accept()
            download.finished.connect(lambda: self.download_finished(path))
            print(f"Downloading: {path}")
        else:
            download.cancel()

    def download_finished(self, path):
        QMessageBox.information(self, "Download Complete", f"File saved to:\n{path}")
        print(f"Download complete: {path}")

# -----------------------------------------------------------------------------


if __name__ == "__main__":
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    window = Browser()
    window.show()
    sys.exit(app.exec_())
