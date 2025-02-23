import sys
from datetime import datetime
from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                            QLabel, QStyle, QStyleFactory, QHBoxLayout,
                            QStackedWidget, QPushButton)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QColor
from PyQt6.QtWidgets import QGraphicsDropShadowEffect
from .navigation import NavigationBar
from .pages.home import HomePage
from .pages.monitor import MonitorPage
from .pages.process import ProcessPage
from .pages.cleaner import CleanerPage
from .pages.settings import SettingsPage

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plug-in box")
        self.setGeometry(100, 100, 900, 600)
        
        # 设置Windows 11风格
        self.setStyle(QStyleFactory.create("Fusion"))
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        
        # 创建主窗口部件
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        # 创建水平布局作为主布局
        self.main_layout = QHBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)
        self.central_widget.setLayout(self.main_layout)
        
        # 创建导航栏
        self.nav_bar = NavigationBar()
        
        # 创建堆叠式布局
        self.stacked_widget = QStackedWidget()
        
        # 创建所有页面
        self.home_page = HomePage()
        self.monitor_page = MonitorPage()
        self.process_page = ProcessPage()
        self.network_page = CleanerPage()
        self.settings_page = SettingsPage()
        
        # 将页面添加到堆叠式布局
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.monitor_page)
        self.stacked_widget.addWidget(self.process_page)
        self.stacked_widget.addWidget(self.network_page)
        self.stacked_widget.addWidget(self.settings_page)
        
        # 将导航栏和堆叠式布局添加到主布局
        self.main_layout.addWidget(self.nav_bar)
        self.main_layout.addWidget(self.stacked_widget)
        
        # 连接导航按钮的信号
        nav_buttons = self.nav_bar.findChildren(QPushButton)
        for i, button in enumerate(nav_buttons):
            button.clicked.connect(lambda checked, index=i: self.stacked_widget.setCurrentIndex(index))
        
        # 设置默认页面
        nav_buttons[0].setChecked(True)
        self.stacked_widget.setCurrentIndex(0)
        
        # 设置窗口样式
        self.setStyleSheet("""
            QMainWindow {
                background-color: #202020;
                border-radius: 12px;
                border: 1px solid rgba(255, 255, 255, 0.1);
            }
            QWidget {
                background-color: #202020;
                color: white;
            }
            #central_widget {
                background: transparent;
                border-radius: 12px;
            }
        """)
        
        # 设置窗口阴影效果
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(20)
        shadow.setColor(QColor(0, 0, 0, 100))
        shadow.setOffset(0, 0)
        self.setGraphicsEffect(shadow)
        
        # 设置默认字体
        font = QFont("Segoe UI", 9)
        self.setFont(font)
        
        # 设置图标
        self.setWindowIcon(QIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_ComputerIcon)))