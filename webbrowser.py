# -*- coding: utf-8 -*-
"""
Created on Sun Oct 12 14:23:06 2025

@author: deepj
"""

from PyQt5.QtWidgets import (QApplication, QMainWindow, QLineEdit, QToolBar, QAction,
                             QTabWidget, QWidget, QVBoxLayout, QMenu, QListWidget, QDockWidget, QFileDialog)
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEngineScript
from PyQt5.QtCore import QUrl, Qt
import sys

class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Light Browser")
        self.setGeometry(100, 100, 1300, 900)

        # Data stores
        self.bookmarks = []
        self.history = []

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.setMovable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.duplicate_tab)
        self.tabs.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabs.customContextMenuRequested.connect(self.tab_context_menu)
        self.tabs.currentChanged.connect(self.update_url)
        self.setCentralWidget(self.tabs)

        # Toolbar
        self.toolbar = QToolBar()
        self.addToolBar(self.toolbar)

        # Navigation Buttons
        back_btn = QAction("Back", self)
        back_btn.triggered.connect(lambda: self.current_browser().back())
        self.toolbar.addAction(back_btn)

        forward_btn = QAction("Forward", self)
        forward_btn.triggered.connect(lambda: self.current_browser().forward())
        self.toolbar.addAction(forward_btn)

        reload_btn = QAction("Reload", self)
        reload_btn.triggered.connect(lambda: self.current_browser().reload())
        self.toolbar.addAction(reload_btn)

        new_tab_btn = QAction("New Tab", self)
        new_tab_btn.triggered.connect(self.add_tab)
        self.toolbar.addAction(new_tab_btn)

        incognito_btn = QAction("Incognito", self)
        incognito_btn.triggered.connect(lambda: self.add_tab(incognito=True))
        self.toolbar.addAction(incognito_btn)

        # Bookmark Button
        bookmark_btn = QAction("Bookmark", self)
        bookmark_btn.triggered.connect(self.add_bookmark)
        self.toolbar.addAction(bookmark_btn)

        # Show Bookmarks
        show_bookmarks_btn = QAction("Bookmarks", self)
        show_bookmarks_btn.triggered.connect(self.show_bookmarks)
        self.toolbar.addAction(show_bookmarks_btn)

        # Show History
        show_history_btn = QAction("History", self)
        show_history_btn.triggered.connect(self.show_history)
        self.toolbar.addAction(show_history_btn)

        # Dark/Light Mode
        theme_btn = QAction("Toggle Theme", self)
        theme_btn.triggered.connect(self.toggle_theme)
        self.toolbar.addAction(theme_btn)
        self.dark_mode = False

        # URL Bar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_to_url)
        self.toolbar.addWidget(self.url_bar)

        # ----------------- AdBlock Script -----------------
        self.adblock_script = QWebEngineScript()
        self.adblock_script.setName("AdBlocker")
        self.adblock_script.setInjectionPoint(QWebEngineScript.DocumentReady)
        self.adblock_script.setRunsOnSubFrames(True)
        self.adblock_script.setWorldId(QWebEngineScript.MainWorld)
        self.adblock_script.setSourceCode("""
            var ads = document.querySelectorAll('[id*="ad"], [class*="ad"], iframe[src*="ads"]');
            ads.forEach(ad => ad.remove());
        """)

        # Add initial tab
        self.add_tab(QUrl("https://www.google.com"))

        # Keyboard shortcuts
        self.toolbar.addAction(QAction("Ctrl+T: New Tab", self, shortcut="Ctrl+T", triggered=self.add_tab))
        self.toolbar.addAction(QAction("Ctrl+W: Close Tab", self, shortcut="Ctrl+W", triggered=lambda: self.close_tab(self.tabs.currentIndex())))
        self.toolbar.addAction(QAction("Ctrl+R: Reload", self, shortcut="Ctrl+R", triggered=lambda: self.current_browser().reload()))

    # ----------------- Browser Helpers -----------------
    def current_browser(self):
        return self.tabs.currentWidget().findChild(QWebEngineView)

    def add_tab(self, url=QUrl("https://www.google.com"), incognito=False):
        profile = QWebEngineProfile.defaultProfile() if not incognito else QWebEngineProfile()
        profile.setPersistentCookiesPolicy(QWebEngineProfile.NoPersistentCookies)
        if incognito:
            profile.setPersistentStoragePath("")  # Avoid disk storage for incognito
        # Insert adblock script
        profile.scripts().insert(self.adblock_script)

        new_tab = QWidget()
        layout = QVBoxLayout()
        webview = QWebEngineView()
        webview.setPage(webview.page().__class__(profile, webview))
        webview.setUrl(url)
        webview.urlChanged.connect(self.update_url)
        webview.loadFinished.connect(self.add_history)
        webview.page().profile().downloadRequested.connect(self.download_file)
        layout.addWidget(webview)
        new_tab.setLayout(layout)
        index = self.tabs.addTab(new_tab, "New Tab" + (" (Incognito)" if incognito else ""))
        self.tabs.setCurrentIndex(index)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)

    def duplicate_tab(self, index):
        browser = self.tabs.widget(index).findChild(QWebEngineView)
        if browser:
            self.add_tab(QUrl(browser.url()))

    def tab_context_menu(self, pos):
        menu = QMenu()
        menu.addAction("Reload", lambda: self.current_browser().reload())
        menu.addAction("Close Tab", lambda: self.close_tab(self.tabs.currentIndex()))
        menu.addAction("Duplicate Tab", lambda: self.duplicate_tab(self.tabs.currentIndex()))
        menu.exec_(self.tabs.mapToGlobal(pos))

    def navigate_to_url(self):
        url = self.url_bar.text()
        if not url.startswith("http"):
            url = "http://" + url
        self.current_browser().setUrl(QUrl(url))

    def update_url(self, _=None):
        browser = self.current_browser()
        if browser:
            self.url_bar.setText(browser.url().toString())
            self.tabs.setTabText(self.tabs.currentIndex(), browser.title() or "New Tab")

    # ----------------- Bookmarks -----------------
    def add_bookmark(self):
        browser = self.current_browser()
        url = browser.url().toString()
        title = browser.title()
        self.bookmarks.append({"title": title, "url": url})
        print(f"Bookmarked: {title} - {url}")

    def show_bookmarks(self):
        dock = QDockWidget("Bookmarks", self)
        list_widget = QListWidget()
        for bm in self.bookmarks:
            list_widget.addItem(f"{bm['title']} - {bm['url']}")
        list_widget.itemDoubleClicked.connect(lambda item: self.current_browser().setUrl(QUrl(item.text().split(" - ")[1])))
        dock.setWidget(list_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    # ----------------- History -----------------
    def add_history(self):
        browser = self.current_browser()
        url = browser.url().toString()
        if url not in self.history:
            self.history.append(url)
            print(f"Visited: {url}")

    def show_history(self):
        dock = QDockWidget("History", self)
        list_widget = QListWidget()
        for url in self.history:
            list_widget.addItem(url)
        list_widget.itemDoubleClicked.connect(lambda item: self.current_browser().setUrl(QUrl(item.text())))
        dock.setWidget(list_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

    # ----------------- Download Manager -----------------
    def download_file(self, download_item):
        path, _ = QFileDialog.getSaveFileName(self, "Save File", download_item.path())
        if path:
            download_item.setPath(path)
            download_item.accept()

    # ----------------- Dark/Light Mode -----------------
    def toggle_theme(self):
        if self.dark_mode:
            self.setStyleSheet("")  # Light mode
        else:
            self.setStyleSheet("QMainWindow { background-color: #121212; color: white; } QToolBar { background-color: #1f1f1f; }")
        self.dark_mode = not self.dark_mode

# ----------------- Run App -----------------
app = QApplication(sys.argv)
window = Browser()
window.show()
sys.exit(app.exec_())
