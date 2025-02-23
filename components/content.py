from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from datetime import datetime

class ContentArea(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建垂直布局
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(20, 10, 20, 10)
        self.layout.setSpacing(10)
        self.setLayout(self.layout)
        
        # 创建更新信息标签
        self.version_label = QLabel("系统工具箱 v1.0.0")
        self.update_time_label = QLabel(f"最后更新时间：{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.description_label = QLabel("这是一个简单的系统工具箱，提供系统监控和维护功能。")
        
        # 添加标签到布局
        self.layout.addWidget(self.version_label)
        self.layout.addWidget(self.update_time_label)
        self.layout.addWidget(self.description_label)
        self.layout.addStretch()
        
        # 设置样式
        self.setStyleSheet("""
            QLabel {
                background: rgba(255, 255, 255, 0.05);
                padding: 15px;
                border-radius: 12px;
                margin: 4px 0;
                font-size: 14px;
                color: white;
                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            }
            QLabel:hover {
                background: rgba(255, 255, 255, 0.08);
                margin-top: 2px;
                margin-bottom: 6px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            }
        """)
        
        # 设置标签样式
        self.version_label.setStyleSheet(self.version_label.styleSheet() + """
            font-weight: bold;
            font-size: 16px;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0.1), rgba(255, 255, 255, 0.05));
        """)
        
        # 设置更新时间标签样式
        self.update_time_label.setStyleSheet(self.update_time_label.styleSheet() + """
            color: rgba(255, 255, 255, 0.7);
        """)