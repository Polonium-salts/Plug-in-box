from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QGridLayout
from PyQt6.QtCore import Qt, QTimer
import platform
import psutil
import cpuinfo
import wmi
import sys

class MonitorPage(QWidget):
    def __init__(self):
        super().__init__()
        self.wmi = wmi.WMI()
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_system_info)
        self.timer.start(30000)  # 每30秒更新一次
        self.info_labels = {}
        self.cached_info = {}
        
        # 创建主布局
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        self.setLayout(main_layout)
        
        # 创建滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: rgba(255, 255, 255, 0.1);
                width: 8px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: rgba(255, 255, 255, 0.2);
                min-height: 20px;
                border-radius: 4px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # 创建内容容器
        content_widget = QWidget()
        content_layout = QVBoxLayout(content_widget)
        content_layout.setSpacing(10)
        scroll_area.setWidget(content_widget)
        
        # 创建网格布局用于放置信息卡片
        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)
        
        # 获取系统信息
        system_info = {
            "操作系统": f"{platform.system()} {platform.version()}",
            "系统架构": platform.machine(),
            "计算机名": platform.node(),
            "系统版本": platform.platform(),
            "系统启动时间": f"{round(psutil.boot_time() / (60*60*24), 1)} 天",
            "Python版本": f"{sys.version}"
        }
        
        # 获取CPU详细信息
        cpu_info = cpuinfo.get_cpu_info()
        cpu_details = {
            "处理器": cpu_info['brand_raw'],
            "架构": cpu_info['arch'],
            "位数": f"{cpu_info['bits']}位",
            "核心数": f"{psutil.cpu_count()} 核心",
            "物理核心数": f"{psutil.cpu_count(logical=False)} 核心",
            "基础频率": f"{cpu_info.get('hz_advertised_friendly', '未知')}",
            "缓存大小": f"{cpu_info.get('l3_cache_size', '未知')} bytes",
            "指令集": ", ".join(cpu_info.get('flags', [])[:5])
        }
        
        # 获取内存详细信息
        memory = psutil.virtual_memory()
        try:
            memory_info = self.wmi.Win32_PhysicalMemory()[0]
            memory_details = {
                "内存总量": f"{round(memory.total / (1024**3), 2)} GB",
                "可用内存": f"{round(memory.available / (1024**3), 2)} GB",
                "内存类型": memory_info.MemoryType,
                "内存频率": f"{memory_info.Speed} MHz",
                "制造商": memory_info.Manufacturer,
                "序列号": memory_info.SerialNumber
            }
        except:
            memory_details = {
                "内存总量": f"{round(memory.total / (1024**3), 2)} GB",
                "可用内存": f"{round(memory.available / (1024**3), 2)} GB"
            }
        
        # 获取显卡详细信息
        gpu_details = {}
        try:
            for gpu in self.wmi.Win32_VideoController():
                gpu_details.update({
                    "显卡型号": gpu.Name,
                    "显存大小": f"{round(int(gpu.AdapterRAM if gpu.AdapterRAM else 0) / (1024**3), 2)} GB",
                    "驱动版本": gpu.DriverVersion,
                    "显示模式": f"{gpu.CurrentHorizontalResolution}x{gpu.CurrentVerticalResolution}",
                    "刷新率": f"{gpu.CurrentRefreshRate}Hz" if gpu.CurrentRefreshRate else "未知",
                    "驱动日期": gpu.DriverDate
                })
        except:
            gpu_details["显卡信息"] = "无法获取显卡信息"
        
        # 获取主板详细信息
        try:
            board = self.wmi.Win32_BaseBoard()[0]
            bios = self.wmi.Win32_BIOS()[0]
            motherboard_details = {
                "主板制造商": board.Manufacturer,
                "主板型号": board.Product,
                "序列号": board.SerialNumber,
                "BIOS版本": bios.Version,
                "BIOS制造商": bios.Manufacturer,
                "BIOS日期": bios.ReleaseDate
            }
        except:
            motherboard_details = {"主板信息": "无法获取主板信息"}
        
        # 获取磁盘详细信息
        disk_details = {}
        try:
            for disk in self.wmi.Win32_DiskDrive():
                disk_details[f"磁盘 {disk.Index}"] = {
                    "型号": disk.Model,
                    "接口类型": disk.InterfaceType,
                    "容量": f"{round(int(disk.Size) / (1024**3), 2)} GB",
                    "分区数": disk.Partitions,
                    "序列号": disk.SerialNumber
                }
        except:
            disk_details["磁盘信息"] = "无法获取磁盘信息"
        
        # 获取网络适配器信息
        network_details = {}
        try:
            for nic in self.wmi.Win32_NetworkAdapter(PhysicalAdapter=True):
                network_details[nic.Name] = {
                    "制造商": nic.Manufacturer,
                    "MAC地址": nic.MACAddress,
                    "适配器类型": nic.AdapterType,
                    "速度": f"{round(int(nic.Speed if nic.Speed else 0) / (1000000), 0)} Mbps" if nic.Speed else "未知"
                }
        except:
            network_details["网络适配器"] = "无法获取网络适配器信息"
        
        # 创建信息卡片
        self._create_info_card(grid_layout, 0, 0, "系统信息", system_info)
        self._create_info_card(grid_layout, 0, 1, "CPU信息", cpu_details)
        self._create_info_card(grid_layout, 1, 0, "内存信息", memory_details)
        self._create_info_card(grid_layout, 1, 1, "显卡信息", gpu_details)
        self._create_info_card(grid_layout, 2, 0, "主板信息", motherboard_details)
        
        # 初始化缓存
        self.cached_info = {
            "system_info": system_info,
            "cpu_details": cpu_details,
            "memory_details": memory_details,
            "gpu_details": gpu_details,
            "motherboard_details": motherboard_details,
            "disk_details": disk_details,
            "network_details": network_details
        }
        
        # 为磁盘和网络信息创建单独的卡片
        disk_layout = QVBoxLayout()
        for disk_name, disk_info in disk_details.items():
            if isinstance(disk_info, dict):
                self._create_info_card(disk_layout, 0, 0, disk_name, disk_info)
            else:
                self._create_info_card(disk_layout, 0, 0, "磁盘信息", {"状态": disk_info})
        
        network_layout = QVBoxLayout()
        for adapter_name, adapter_info in network_details.items():
            if isinstance(adapter_info, dict):
                self._create_info_card(network_layout, 0, 0, adapter_name, adapter_info)
            else:
                self._create_info_card(network_layout, 0, 0, "网络信息", {"状态": adapter_info})
        
        content_layout.addLayout(grid_layout)
        content_layout.addLayout(disk_layout)
        content_layout.addLayout(network_layout)
        main_layout.addWidget(scroll_area)
    
    def update_system_info(self):
        try:
            # 更新内存信息
            memory = psutil.virtual_memory()
            try:
                memory_info = self.wmi.Win32_PhysicalMemory()[0]
                new_memory_details = {
                    "内存总量": f"{round(memory.total / (1024**3), 2)} GB",
                    "可用内存": f"{round(memory.available / (1024**3), 2)} GB",
                    "内存类型": memory_info.MemoryType,
                    "内存频率": f"{memory_info.Speed} MHz",
                    "制造商": memory_info.Manufacturer,
                    "序列号": memory_info.SerialNumber
                }
            except:
                new_memory_details = {
                    "内存总量": f"{round(memory.total / (1024**3), 2)} GB",
                    "可用内存": f"{round(memory.available / (1024**3), 2)} GB"
                }
            
            # 更新显示
            if str(new_memory_details) != str(self.cached_info.get("memory_details")):
                self.cached_info["memory_details"] = new_memory_details
                for key, value in new_memory_details.items():
                    if key in self.info_labels:
                        self.info_labels[key].setText(str(value))
        except Exception as e:
            print(f"更新系统信息时出错：{str(e)}")
    
    def _create_info_card(self, layout, row, col, title, info_dict):
        card = QWidget()
        card.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 12px;
            }
        """)
        
        card_layout = QVBoxLayout(card)
        card_layout.setSpacing(8)
        card_layout.setContentsMargins(12, 12, 12, 12)
        
        # 添加标题
        title_label = QLabel(title)
        title_label.setStyleSheet("""
            color: white;
            font-size: 14px;
            font-weight: bold;
            padding-bottom: 8px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        """)
        card_layout.addWidget(title_label)
        
        # 添加信息项
        for key, value in info_dict.items():
            item_widget = QWidget()
            item_layout = QHBoxLayout(item_widget)
            item_layout.setContentsMargins(0, 0, 0, 0)
            item_layout.setSpacing(8)
            
            key_label = QLabel(key)
            key_label.setStyleSheet("""
                color: rgba(255, 255, 255, 0.7);
                font-size: 12px;
            """)
            
            value_label = QLabel(str(value))
            value_label.setStyleSheet("""
                color: white;
                font-size: 12px;
            """)
            value_label.setWordWrap(True)
            
            item_layout.addWidget(key_label)
            item_layout.addWidget(value_label, 1)
            
            card_layout.addWidget(item_widget)
        
        if isinstance(layout, QGridLayout):
            layout.addWidget(card, row, col)
        else:
            layout.addWidget(card)