from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit, QHBoxLayout
from PyQt6.QtCore import Qt
import subprocess
import socket
import platform

class NetworkPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # 创建标题
        title = QLabel("网络工具")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # 创建Ping测试区域
        ping_container = QWidget()
        ping_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        ping_layout = QVBoxLayout()
        ping_container.setLayout(ping_layout)
        
        # Ping输入区域
        ping_input_layout = QHBoxLayout()
        self.ping_input = QLineEdit()
        self.ping_input.setPlaceholderText("输入要测试的域名或IP地址")
        self.ping_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px;
            }
        """)
        ping_button = QPushButton("Ping测试")
        ping_button.setStyleSheet("""
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
        ping_input_layout.addWidget(self.ping_input)
        ping_input_layout.addWidget(ping_button)
        
        # Ping结果显示区域
        self.ping_result = QTextEdit()
        self.ping_result.setReadOnly(True)
        self.ping_result.setStyleSheet("""
            QTextEdit {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px;
            }
        """)
        
        ping_layout.addLayout(ping_input_layout)
        ping_layout.addWidget(self.ping_result)
        layout.addWidget(ping_container)
        
        # 创建网络信息显示区域
        info_container = QWidget()
        info_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        info_layout = QVBoxLayout()
        info_container.setLayout(info_layout)
        
        # 获取并显示网络信息
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        
        info_layout.addWidget(QLabel(f"主机名：{hostname}"))
        info_layout.addWidget(QLabel(f"IP地址：{ip_address}"))
        
        layout.addWidget(info_container)
        
        # 添加底部弹簧
        layout.addStretch()
        
        # 连接信号
        ping_button.clicked.connect(self.do_ping)
    
    def do_ping(self):
        target = self.ping_input.text().strip()
        if not target:
            return
        
        self.ping_result.clear()
        try:
            if platform.system().lower() == 'windows':
                process = subprocess.Popen(['ping', '-n', '4', target],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True)
            else:
                process = subprocess.Popen(['ping', '-c', '4', target],
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE,
                                         text=True)
            
            stdout, stderr = process.communicate()
            if stderr:
                self.ping_result.setText(f"错误：{stderr}")
            else:
                self.ping_result.setText(stdout)
        except Exception as e:
            self.ping_result.setText(f"执行Ping测试时出错：{str(e)}")