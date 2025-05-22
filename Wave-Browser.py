import sys
import re
from urllib.parse import quote
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QTabWidget, QPushButton,
    QWidget, QVBoxLayout, QHBoxLayout, QLineEdit
)
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt
from PyQt6.QtGui import QIcon


class Browser(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Wave Browser")
        self.setWindowIcon(QIcon('icon.png'))

        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        self.tabs.tabBarDoubleClicked.connect(self.handle_double_click)

        self.setup_ui()
        self.add_new_tab()
        self.showMaximized()

    def setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(self.tabs)

        new_tab_btn = QPushButton("+")
        new_tab_btn.setStyleSheet(self.new_tab_button_style())
        new_tab_btn.clicked.connect(self.add_new_tab)

        corner_widget = QWidget()
        corner_layout = QHBoxLayout(corner_widget)
        corner_layout.setContentsMargins(4, 0, 0, 0)
        corner_layout.setSpacing(0)
        corner_layout.addWidget(new_tab_btn)

        self.tabs.setCornerWidget(corner_widget, Qt.Corner.TopLeftCorner)

    def new_tab_button_style(self):
        return """
            QPushButton {
                border: none;
                padding: 8px 16px;
                font-size: 16px;
                font-weight: 500;
                color: #5f6368;
                background: transparent;
                margin: 0;
                height: 36px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background: rgba(32, 33, 36, 0.1);
            }
            QPushButton:pressed {
                background: rgba(32, 33, 36, 0.15);
            }
        """

    def add_new_tab(self, url='https://unblocker-bpqg.onrender.com'):
        tab = QWidget()
        layout = QVBoxLayout(tab)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        nav_bar = QHBoxLayout()
        nav_bar.setContentsMargins(6, 6, 6, 0)

        back_btn = QPushButton("←")
        forward_btn = QPushButton("→")
        search_bar = QLineEdit()
        search_bar.setPlaceholderText("Search or enter address")

        for btn in (back_btn, forward_btn):
            btn.setFixedWidth(30)
            btn.setStyleSheet("""
                QPushButton {
                    border: none;
                    font-size: 16px;
                    padding: 4px;
                    background: #f1f3f4;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background: #e0e0e0;
                }
            """)

        search_bar.setStyleSheet("""
            QLineEdit {
                padding: 6px;
                font-size: 14px;
                border: 1px solid #ccc;
                border-radius: 4px;
                flex-grow: 1;
            }
        """)

        nav_bar.addWidget(back_btn)
        nav_bar.addWidget(forward_btn)
        nav_bar.addWidget(search_bar)

        web_view = QWebEngineView()
        web_view.setStyleSheet("QWebEngineView { background: black; }")
        web_view.setUrl(QUrl(url))

        layout.addLayout(nav_bar)
        layout.addWidget(web_view)

        index = self.tabs.addTab(tab, "New Tab")
        self.tabs.setCurrentIndex(index)

        # Connect functionality
        search_bar.returnPressed.connect(lambda: self.navigate_to_url(search_bar, web_view))
        back_btn.clicked.connect(web_view.back)
        forward_btn.clicked.connect(web_view.forward)
        web_view.urlChanged.connect(lambda url: search_bar.setText(url.toString()))
        web_view.titleChanged.connect(lambda title, i=index: self.tabs.setTabText(i, title))
        web_view.iconChanged.connect(lambda icon, i=index: self.tabs.setTabIcon(i, icon))

    def navigate_to_url(self, search_bar, web_view):
        text = search_bar.text().strip()
        if not text:
            return

        if re.match(r'^[a-zA-Z]+://', text):
            url = QUrl(text)
        elif '.' in text and ' ' not in text:
            url = QUrl(f"http://{text}")
        else:
            query = quote(text)
            url = QUrl(f'https://www.google.com/search?q={query}')

        if url.isValid():
            web_view.setUrl(url)

    def close_tab(self, index):
        if self.tabs.count() > 1:
            self.tabs.removeTab(index)
        else:
            QApplication.quit()

    def handle_double_click(self, index):
        if index == -1:
            self.add_new_tab()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = Browser()
    sys.exit(app.exec())
