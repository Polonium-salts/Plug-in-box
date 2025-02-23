from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt
from datetime import datetime

class HomePage(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建垂直布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # 创建欢迎标题
        welcome_label = QLabel("欢迎使用Plug-in box")
        welcome_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 10px;
        """)
        
        # 创建版本信息
        version_label = QLabel("版本 1.2.0")
        version_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        version_label.setStyleSheet("""
            font-size: 14px;
            color: rgba(255, 255, 255, 0.7);
            margin-bottom: 20px;
        """)
        
        # 创建功能介绍
        features = [
            "系统监控：实时监控CPU、内存、显卡等硬件信息",
            "驱动管理：检测和管理系统驱动程序",
            "网络工具：网络连接测试和IP配置",
            "系统设置：主题切换和自动启动设置"
        ]
        
        # 添加组件到布局
        layout.addWidget(welcome_label)
        layout.addWidget(version_label)
        
        # 添加功能介绍
        for feature in features:
            feature_label = QLabel(feature)
            feature_label.setStyleSheet("""
                background: rgba(255, 255, 255, 0.05);
                padding: 15px;
                border-radius: 10px;
                color: white;
                font-size: 14px;
            """)
            layout.addWidget(feature_label)
        
        # 添加底部弹簧
        layout.addStretch()
        
        # 添加更新时间
        update_label = QLabel(f"最后更新：{datetime.now().strftime('%Y-%m-%d')}")
        update_label.setAlignment(Qt.AlignmentFlag.AlignRight)
        update_label.setStyleSheet("""
            color: rgba(255, 255, 255, 0.5);
            font-size: 12px;
        """)
        layout.addWidget(update_label)