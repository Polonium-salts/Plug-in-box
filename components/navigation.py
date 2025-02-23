from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
import os

class NavigationBar(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedWidth(160)
        
        # 创建垂直布局
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(12, 20, 12, 20)
        self.layout.setSpacing(6)
        self.setLayout(self.layout)
        
        # 创建标题标签
        self.title_label = QLabel("Plug-in box")
        self.title_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 16px;
                font-weight: bold;
                padding: 5px;
                margin-bottom: 10px;
            }
        """)
        self.layout.insertWidget(0, self.title_label)
        
        # 导航按钮配置
        nav_buttons = [
            ("主页", "home.svg"),
            ("系统信息", "monitor.svg"),
            ("驱动安装", "process.svg"),
            ("垃圾清理", "network.svg"),
            ("系统设置", "settings.svg")
        ]
        
        # 创建导航按钮
        for text, icon_file in nav_buttons:
            btn = QPushButton(text)
            icon_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "icons", icon_file)
            btn.setIcon(QIcon(icon_path))
            btn.setIconSize(btn.iconSize() * 1.2)
            btn.setCheckable(True)
            btn.setAutoExclusive(True)
            self.layout.addWidget(btn)
        
        # 添加底部弹簧
        self.layout.addStretch()
        
        # 设置样式
        self.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
                text-align: left;
                font-size: 14px;
                color: white;
                margin: 2px 0;
                font-weight: 500;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
                margin-left: 2px;
            }
            QPushButton:checked {
                background: rgba(255, 255, 255, 0.15);
                font-weight: bold;
            }
        """)
        
        # 添加右侧边框
        self.setStyleSheet(self.styleSheet() + """
            NavigationBar {
                border-right: 1px solid rgba(255, 255, 255, 0.1);
            }
        """)