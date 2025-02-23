from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QCheckBox, QComboBox, QHBoxLayout, QPushButton
from PyQt6.QtCore import Qt

class SettingsPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # 创建标题
        title = QLabel("系统设置")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # 创建设置项容器
        settings_container = QWidget()
        settings_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        settings_layout = QVBoxLayout()
        settings_container.setLayout(settings_layout)
        
        # 自动启动设置
        auto_start = QCheckBox("开机自动启动")
        auto_start.setStyleSheet("""
            QCheckBox {
                color: white;
                font-size: 14px;
                padding: 8px;
            }
            QCheckBox::indicator {
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 2px solid rgba(255, 255, 255, 0.3);
            }
            QCheckBox::indicator:checked {
                background: #4CAF50;
                border: 2px solid #4CAF50;
            }
        """)
        
        # 主题选择
        theme_layout = QHBoxLayout()
        theme_label = QLabel("主题：")
        theme_label.setStyleSheet("color: white; font-size: 14px;")
        theme_combo = QComboBox()
        theme_combo.addItems(["深色", "浅色"])
        theme_combo.setStyleSheet("""
            QComboBox {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
            }
        """)
        theme_layout.addWidget(theme_label)
        theme_layout.addWidget(theme_combo)
        theme_layout.addStretch()
        
        # 更新设置
        update_layout = QHBoxLayout()
        update_label = QLabel("检查更新：")
        update_label.setStyleSheet("color: white; font-size: 14px;")
        update_button = QPushButton("检查更新")
        update_button.setStyleSheet("""
            QPushButton {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background: rgba(255, 255, 255, 0.15);
            }
        """)
        update_layout.addWidget(update_label)
        update_layout.addWidget(update_button)
        update_layout.addStretch()
        
        # 添加设置项到容器
        settings_layout.addWidget(auto_start)
        settings_layout.addLayout(theme_layout)
        settings_layout.addLayout(update_layout)
        
        # 添加设置容器到主布局
        layout.addWidget(settings_container)
        
        # 添加保存按钮
        save_button = QPushButton("保存设置")
        save_button.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                margin-top: 20px;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        layout.addWidget(save_button)
        
        # 添加底部弹簧
        layout.addStretch()