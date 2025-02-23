from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QListWidgetItem,
                         QPushButton, QHBoxLayout, QLineEdit, QApplication)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QIcon, QColor
import wmi
import os
import time

class ProcessPage(QWidget):
    def __init__(self):
        super().__init__()
        self.wmi = wmi.WMI()
        self.cached_drivers = None
        self.last_update_time = 0
        self.update_interval = 30  # 更新间隔（秒）
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # 创建标题
        title = QLabel("驱动检测")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # 创建搜索框
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("搜索驱动...")
        self.search_input.setStyleSheet("""
            QLineEdit {
                background: rgba(255, 255, 255, 0.1);
                border: none;
                border-radius: 5px;
                color: white;
                padding: 8px;
            }
        """)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # 创建驱动列表
        self.driver_list = QListWidget()
        self.driver_list.setStyleSheet("""
            QListWidget {
                background: rgba(255, 255, 255, 0.05);
                border: none;
                border-radius: 10px;
                color: white;
                padding: 5px;
            }
            QListWidget::item {
                background: rgba(255, 255, 255, 0.02);
                border-radius: 5px;
                padding: 10px;
                margin: 2px 5px;
            }
            QListWidget::item:hover {
                background: rgba(255, 255, 255, 0.05);
            }
            QListWidget::item:selected {
                background: rgba(255, 255, 255, 0.1);
            }
        """)
        layout.addWidget(self.driver_list)
        
        # 创建按钮区域
        button_layout = QHBoxLayout()
        refresh_button = QPushButton("刷新")
        scan_button = QPushButton("扫描缺失驱动")
        
        button_style = """
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
        """
        
        refresh_button.setStyleSheet(button_style)
        scan_button.setStyleSheet(button_style)
        
        button_layout.addWidget(refresh_button)
        button_layout.addWidget(scan_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
        
        # 连接信号
        refresh_button.clicked.connect(self.update_driver_list)
        scan_button.clicked.connect(self.scan_missing_drivers)
        self.search_input.textChanged.connect(self.filter_drivers)
        
        # 移除自动更新定时器，改为手动触发
        # self.timer = QTimer()
        # self.timer.timeout.connect(self.update_driver_list)
        # self.timer.start(30000)  # 每30秒更新一次
        
        # 初始化驱动列表
        # self.update_driver_list()
    
    def update_driver_list(self):
        try:
            current_time = time.time()
            # 检查是否需要更新缓存
            if self.cached_drivers is None or (current_time - self.last_update_time) >= self.update_interval:
                # 获取驱动信息
                self.cached_drivers = list(self.wmi.Win32_SystemDriver())
                self.last_update_time = current_time
            
            # 清空列表
            self.driver_list.clear()
            
            # 使用缓存的驱动信息
            for driver in self.cached_drivers:
                try:
                    # 创建列表项
                    item = QListWidgetItem()
                    
                    # 设置驱动信息，添加错误处理
                    name = str(driver.Name if hasattr(driver, 'Name') else '未知')
                    version = str(driver.Version if hasattr(driver, 'Version') else '未知')
                    manufacturer = str(driver.Manufacturer if hasattr(driver, 'Manufacturer') else '未知')
                    state = str(driver.State if hasattr(driver, 'State') else '未知')
                    path = str(driver.PathName if hasattr(driver, 'PathName') else '未知')
                    description = str(driver.Description if hasattr(driver, 'Description') else '未知')
                    start_mode = str(driver.StartMode if hasattr(driver, 'StartMode') else '未知')
                    status = str(driver.Status if hasattr(driver, 'Status') else '未知')
                    
                    # 创建显示文本
                    display_text = f"名称: {name}\n版本: {version}\n发布商: {manufacturer}\n状态: {state}\n启动类型: {start_mode}\n路径: {path}\n描述: {description}\n运行状态: {status}"
                    item.setText(display_text)
                    
                    # 设置状态颜色
                    if state == "Running":
                        item.setForeground(QColor("#4CAF50"))  # 绿色
                    elif state == "Stopped":
                        item.setForeground(QColor("#F44336"))  # 红色
                    
                    self.driver_list.addItem(item)
                except AttributeError as e:
                    print(f"处理驱动信息时出错：{str(e)}")
                    continue
                
        except Exception as e:
            print(f"更新驱动列表时出错：{str(e)}")
            self.driver_list.clear()
            error_item = QListWidgetItem("获取驱动信息失败，请稍后重试")
            error_item.setForeground(QColor("#F44336"))
            self.driver_list.addItem(error_item)
    
    def filter_drivers(self):
        if self.cached_drivers is None:
            return
            
        search_text = self.search_input.text().lower()
        self.driver_list.clear()
        
        try:
            # 使用缓存的驱动信息进行搜索
            for driver in self.cached_drivers:
                # 检查是否匹配搜索条件
                name = str(driver.Name or "").lower()
                description = str(driver.Description or "").lower()
                manufacturer = str(driver.Manufacturer or "").lower()
                
                if search_text in name or search_text in description or search_text in manufacturer:
                    # 创建列表项
                    item = QListWidgetItem()
                    
                    # 设置驱动信息
                    name = str(driver.Name)
                    version = str(driver.Version or "未知")
                    manufacturer = str(driver.Manufacturer or "未知")
                    state = str(driver.State or "未知")
                    path = str(driver.PathName or "未知")
                    description = str(driver.Description or "未知")
                    start_mode = str(driver.StartMode or "未知")
                    status = str(driver.Status or "未知")
                    
                    # 创建显示文本
                    display_text = f"名称: {name}\n版本: {version}\n发布商: {manufacturer}\n状态: {state}\n启动类型: {start_mode}\n路径: {path}\n描述: {description}\n运行状态: {status}"
                    item.setText(display_text)
                    
                    # 设置状态颜色
                    if state == "Running":
                        item.setForeground(QColor("#4CAF50"))  # 绿色表示运行中
                    elif state == "Stopped":
                        item.setForeground(QColor("#F44336"))  # 红色表示已停止
                    
                    self.driver_list.addItem(item)
                    
        except Exception as e:
            print(f"搜索驱动时出错：{str(e)}")
            self.driver_list.clear()
            error_item = QListWidgetItem("搜索驱动失败，请稍后重试")
            error_item.setForeground(QColor("#F44336"))
            self.driver_list.addItem(error_item)
    
    def scan_missing_drivers(self):
        try:
            self.driver_list.clear()
            # 显示加载提示
            loading_item = QListWidgetItem("正在扫描驱动，请稍候...")
            loading_item.setForeground(QColor("#FFA500"))
            self.driver_list.addItem(loading_item)
            QApplication.processEvents()
            
            # 获取所有设备
            devices = self.wmi.Win32_PnPEntity()
            all_drivers = []
            
            for device in devices:
                # 只处理实际的设备驱动
                if device.ConfigManagerErrorCode is not None:
                    driver_info = {
                        'name': device.Name or "未知",
                        'description': device.Description or "未知",
                        'manufacturer': device.Manufacturer or "未知",
                        'device_id': device.DeviceID or "未知",
                        'driver_version': device.DriverVersion or "未知",
                        'status': device.Status or "未知",
                        'error_code': device.ConfigManagerErrorCode,
                        'is_installed': device.ConfigManagerErrorCode == 0
                    }
                    all_drivers.append(driver_info)
            
            # 显示所有驱动
            self.driver_list.clear()
            if all_drivers:
                # 首先显示未安装的驱动
                uninstalled_drivers = [d for d in all_drivers if not d['is_installed']]
                installed_drivers = [d for d in all_drivers if d['is_installed']]
                
                # 显示未安装驱动
                if uninstalled_drivers:
                    header_item = QListWidgetItem("=== 未安装的驱动 ===")
                    header_item.setForeground(QColor("#FFA500"))
                    self.driver_list.addItem(header_item)
                    
                    for driver in uninstalled_drivers:
                        item = QListWidgetItem()
                        error_desc = self._get_error_description(driver['error_code'])
                        display_text = f"[未安装] 名称: {driver['name']}\n发布商: {driver['manufacturer']}\n版本: {driver['driver_version']}\n描述: {driver['description']}\n状态: {driver['status']}\n问题: {error_desc}"
                        item.setText(display_text)
                        item.setForeground(QColor("#FFA500"))
                        self.driver_list.addItem(item)
                
                # 显示已安装驱动
                if installed_drivers:
                    header_item = QListWidgetItem("\n=== 已安装的驱动 ===")
                    header_item.setForeground(QColor("#4CAF50"))
                    self.driver_list.addItem(header_item)
                    
                    for driver in installed_drivers:
                        item = QListWidgetItem()
                        display_text = f"[已安装] 名称: {driver['name']}\n发布商: {driver['manufacturer']}\n版本: {driver['driver_version']}\n描述: {driver['description']}\n状态: {driver['status']}"
                        item.setText(display_text)
                        item.setForeground(QColor("#4CAF50"))
                        self.driver_list.addItem(item)
            else:
                item = QListWidgetItem("未找到任何驱动信息")
                item.setForeground(QColor("#F44336"))
                self.driver_list.addItem(item)
                
        except Exception as e:
            print(f"扫描驱动时出错：{str(e)}")
            self.driver_list.clear()
            error_item = QListWidgetItem("扫描驱动失败，请稍后重试")
            error_item.setForeground(QColor("#F44336"))
            self.driver_list.addItem(error_item)
    
    def _get_error_description(self, error_code):
        error_codes = {
            1: "设备未配置",
            2: "驱动程序未安装",
            3: "驱动程序损坏",
            4: "设备无法启动",
            5: "设备冲突",
            6: "需要手动配置",
            7: "启动失败",
            8: "固件未响应",
            9: "设备已禁用",
            10: "需要重启系统",
            11: "需要重新枚举",
            12: "无法识别",
            13: "需要重新安装驱动",
            14: "资源冲突",
            15: "需要电源循环",
            16: "设备无法识别",
            17: "设备已禁用",
            18: "设备移除",
            19: "驱动未安装",
            20: "固件更新",
            21: "设备重置",
            22: "资源不足",
            23: "系统故障",
            24: "主机适配器冲突"
        }
        return error_codes.get(error_code, f"未知错误（代码：{error_code}）")