from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPushButton, QProgressBar,
                            QHBoxLayout, QSpacerItem, QSizePolicy, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
import os
import shutil
import tempfile
from pathlib import Path

from concurrent.futures import ThreadPoolExecutor

class ScanThread(QThread):
    progress_updated = pyqtSignal(int, str)
    scan_completed = pyqtSignal(dict)
    
    def __init__(self):
        super().__init__()
        self.system_files_whitelist = [
            'hiberfil.sys',
            'pagefile.sys',
            'swapfile.sys',
            'bootmgr',
            'NTUSER.DAT',
            'ntuser.dat.LOG1',
            'ntuser.dat.LOG2'
        ]
        self.chat_files_whitelist = [
            'All Users',
            'Applet',
            'Avatar',
            'BackupFiles',
            'CommonFiles'
        ]
    
    def run(self):
        results = {}
        total_steps = 14  # 增加了微信和QQ两个步骤
        current_step = 0
        
        # 使用线程池加速扫描
        with ThreadPoolExecutor(max_workers=4) as executor:
            # 扫描系统临时文件
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描系统临时文件...")
            temp_future = executor.submit(self.get_folder_size, tempfile.gettempdir())
            
            # 扫描微信聊天记录
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描微信聊天记录...")
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            wechat_future = executor.submit(self.get_folder_size, wechat_path)
            
            # 扫描QQ聊天记录
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描QQ聊天记录...")
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            qq_future = executor.submit(self.get_folder_size, qq_path)
            
            # 扫描浏览器缓存
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描浏览器缓存...")
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            firefox_cache = os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles')
            browser_future = executor.submit(lambda: (
                self.get_folder_size(chrome_cache) +
                self.get_folder_size(edge_cache) +
                self.get_folder_size(firefox_cache)
            ))
            
            # 扫描Windows更新缓存
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描Windows更新缓存...")
            windows_update = os.path.expandvars('%SystemRoot%\\SoftwareDistribution\\Download')
            update_future = executor.submit(self.get_folder_size, windows_update)
            
            # 扫描系统日志文件
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描系统日志...")
            log_files = os.path.expandvars('%SystemRoot%\\Logs')
            log_future = executor.submit(self.get_folder_size, log_files)
            
            # 扫描应用程序缓存
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描应用程序缓存...")
            app_data = os.path.expanduser('~\\AppData\\Local\\Temp')
            app_cache_future = executor.submit(self.get_folder_size, app_data)
            
            # 扫描Windows错误报告
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描Windows错误报告...")
            error_reports = os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\WER')
            error_future = executor.submit(self.get_folder_size, error_reports)
            
            # 扫描缩略图缓存
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描缩略图缓存...")
            thumbs_db = os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Explorer')
            thumbs_future = executor.submit(self.get_folder_size, thumbs_db)
            
            # 扫描回收站
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描回收站...")
            recycle_bin = os.path.expanduser('~\\$Recycle.Bin')
            recycle_future = executor.submit(self.get_folder_size, recycle_bin)
            
            # 扫描Windows Prefetch文件
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描预读取文件...")
            prefetch = os.path.expandvars('%SystemRoot%\\Prefetch')
            prefetch_future = executor.submit(self.get_folder_size, prefetch)
            
            # 扫描Windows字体缓存
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描字体缓存...")
            font_cache = os.path.expandvars('%SystemRoot%\\ServiceProfiles\\LocalService\\AppData\\Local\\FontCache')
            font_future = executor.submit(self.get_folder_size, font_cache)
            
            # 扫描Windows安装缓存
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描安装缓存...")
            installer_cache = os.path.expandvars('%SystemRoot%\\Installer')
            installer_future = executor.submit(self.get_folder_size, installer_cache)
            
            # 扫描Windows补丁缓存
            current_step += 1
            self.progress_updated.emit(int((current_step/total_steps)*100), "正在扫描系统补丁缓存...")
            patch_cache = os.path.expandvars('%SystemRoot%\\SoftwareDistribution\\Download')
            patch_future = executor.submit(self.get_folder_size, patch_cache)
            
            # 获取所有结果
            results['temp_files'] = temp_future.result()
            results['wechat_files'] = wechat_future.result()
            results['qq_files'] = qq_future.result()
            results['browser_cache'] = browser_future.result()
            results['windows_update'] = update_future.result()
            results['log_files'] = log_future.result()
            results['app_cache'] = app_cache_future.result()
            results['error_reports'] = error_future.result()
            results['thumbs_cache'] = thumbs_future.result()
            results['recycle_bin'] = recycle_future.result()
            results['prefetch'] = prefetch_future.result()
            results['font_cache'] = font_future.result()
            results['installer_cache'] = installer_future.result()
            results['patch_cache'] = patch_future.result()
        
        self.progress_updated.emit(100, "扫描完成")
        self.scan_completed.emit(results)
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size

class CleanerPage(QWidget):
    def __init__(self):
        super().__init__()
        
        # 创建主布局
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        self.setLayout(layout)
        
        # 存储标签引用的字典
        self.info_labels = {}
        
        # 创建标题
        title = QLabel("垃圾清理")
        title.setStyleSheet("""
            font-size: 24px;
            font-weight: bold;
            color: white;
            margin-bottom: 20px;
        """)
        layout.addWidget(title)
        
        # 创建扫描按钮
        scan_button = QPushButton("开始扫描")
        scan_button.setStyleSheet("""
            QPushButton {
                background: #4CAF50;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
            }
            QPushButton:hover {
                background: #45a049;
            }
        """)
        scan_button.clicked.connect(self.scan_junk)
        layout.addWidget(scan_button)
        
        # 创建进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: none;
                border-radius: 5px;
                background: rgba(255, 255, 255, 0.1);
                height: 8px;
                text-align: center;
            }
            QProgressBar::chunk {
                background: #4CAF50;
                border-radius: 5px;
            }
        """)
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        
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
        
        # 创建结果容器
        self.results_container = QWidget()
        self.results_container.setStyleSheet("""
            QWidget {
                background: rgba(255, 255, 255, 0.05);
                border-radius: 10px;
                padding: 15px;
            }
        """)
        results_layout = QVBoxLayout()
        results_layout.setSpacing(8)
        self.results_container.setLayout(results_layout)
        
        # 创建各类垃圾文件显示区域
        self.temp_files_label = self.create_info_label("系统临时文件：")
        self.wechat_files_label = self.create_info_label("微信聊天记录：")
        self.qq_files_label = self.create_info_label("QQ聊天记录：")
        self.browser_cache_label = self.create_info_label("浏览器缓存：")
        self.windows_update_label = self.create_info_label("Windows更新缓存：")
        self.log_files_label = self.create_info_label("系统日志文件：")
        self.app_cache_label = self.create_info_label("应用程序缓存：")
        self.error_reports_label = self.create_info_label("Windows错误报告：")
        self.thumbs_cache_label = self.create_info_label("缩略图缓存：")
        self.recycle_bin_label = self.create_info_label("回收站：")
        self.prefetch_label = self.create_info_label("预读取文件：")
        self.font_cache_label = self.create_info_label("字体缓存：")
        self.installer_cache_label = self.create_info_label("安装缓存：")
        self.patch_cache_label = self.create_info_label("系统补丁缓存：")
        
        results_layout.addWidget(self.temp_files_label)
        results_layout.addWidget(self.wechat_files_label)
        results_layout.addWidget(self.qq_files_label)
        results_layout.addWidget(self.browser_cache_label)
        results_layout.addWidget(self.windows_update_label)
        results_layout.addWidget(self.log_files_label)
        results_layout.addWidget(self.app_cache_label)
        results_layout.addWidget(self.error_reports_label)
        results_layout.addWidget(self.thumbs_cache_label)
        results_layout.addWidget(self.recycle_bin_label)
        results_layout.addWidget(self.prefetch_label)
        results_layout.addWidget(self.font_cache_label)
        results_layout.addWidget(self.installer_cache_label)
        results_layout.addWidget(self.patch_cache_label)
        
        # 设置滚动区域的内容和最大高度
        scroll_area.setWidget(self.results_container)
        scroll_area.setMaximumHeight(400)  # 设置最大高度
        layout.addWidget(scroll_area)
        self.results_container.hide()
        
        # 添加底部弹簧
        layout.addStretch()
        
        # 创建清理按钮
        self.clean_button = QPushButton("一键清理")
        self.clean_button.setStyleSheet("""
            QPushButton {
                background: #F44336;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 10px 20px;
                font-weight: bold;
                margin-top: 10px;
            }
            QPushButton:hover {
                background: #E53935;
            }
        """)
        self.clean_button.clicked.connect(self.clean_junk)
        self.clean_button.hide()
        results_layout.addWidget(self.clean_button)
        
        # 设置滚动区域的内容和最大高度
        scroll_area.setWidget(self.results_container)
        scroll_area.setMaximumHeight(400)  # 设置最大高度
        layout.addWidget(scroll_area)
        self.results_container.hide()
        
        # 添加底部弹簧
        layout.addStretch()
    
    def create_info_label(self, text):
        label = QLabel(text)
        label.setStyleSheet("""
            color: white;
            font-size: 14px;
            padding: 8px;
            margin: 2px 0;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
        """)
        
        delete_button = QPushButton("删除")
        delete_button.setStyleSheet("""
            QPushButton {
                background: #F44336;
                border: none;
                border-radius: 5px;
                color: white;
                padding: 6px 12px;
                font-size: 12px;
            }
            QPushButton:hover {
                background: #E53935;
            }
        """)
        delete_button.setFixedWidth(60)
        
        container = QWidget()
        layout = QHBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)
        layout.addWidget(label, 1)
        layout.addWidget(delete_button)
        
        # 存储标签和按钮的引用
        self.info_labels[text.split('：')[0]] = label
        delete_button.clicked.connect(lambda checked, path=self._get_path_for_label(text): self.clean_specific_folder(path))
        
        return container
    
    def format_size(self, size):
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.2f} {unit}"
            size /= 1024
        return f"{size:.2f} TB"
    
    def scan_junk(self):
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        self.scan_thread = ScanThread()
        self.scan_thread.progress_updated.connect(self.update_progress)
        self.scan_thread.scan_completed.connect(self.update_scan_results)
        self.scan_thread.start()
    
    def update_progress(self, value, status):
        self.progress_bar.setValue(value)
        self.progress_bar.setFormat(f"%p% - {status}")
    
    def update_scan_results(self, results):
        self.info_labels['系统临时文件'].setText(f"系统临时文件：{self.format_size(results['temp_files'])}")
        self.info_labels['微信聊天记录'].setText(f"微信聊天记录：{self.format_size(results['wechat_files'])}")
        self.info_labels['QQ聊天记录'].setText(f"QQ聊天记录：{self.format_size(results['qq_files'])}")
        self.info_labels['浏览器缓存'].setText(f"浏览器缓存：{self.format_size(results['browser_cache'])}")
        self.info_labels['Windows更新缓存'].setText(f"Windows更新缓存：{self.format_size(results['windows_update'])}")
        self.info_labels['系统日志文件'].setText(f"系统日志文件：{self.format_size(results['log_files'])}")
        self.info_labels['应用程序缓存'].setText(f"应用程序缓存：{self.format_size(results['app_cache'])}")
        self.info_labels['Windows错误报告'].setText(f"Windows错误报告：{self.format_size(results['error_reports'])}")
        self.info_labels['缩略图缓存'].setText(f"缩略图缓存：{self.format_size(results['thumbs_cache'])}")
        self.info_labels['回收站'].setText(f"回收站：{self.format_size(results['recycle_bin'])}")
        self.info_labels['预读取文件'].setText(f"预读取文件：{self.format_size(results['prefetch'])}")
        self.info_labels['字体缓存'].setText(f"字体缓存：{self.format_size(results['font_cache'])}")
        self.info_labels['安装缓存'].setText(f"安装缓存：{self.format_size(results['installer_cache'])}")
        self.info_labels['系统补丁缓存'].setText(f"系统补丁缓存：{self.format_size(results['patch_cache'])}")
        self.results_container.show()
        self.clean_button.show()
    
    def clean_junk(self):
        try:
            # 请求管理员权限
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            firefox_cache = os.path.expanduser('~\\AppData\\Local\\Mozilla\\Firefox\\Profiles')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            self.clean_folder(firefox_cache)
            
            # 清理Windows更新缓存
            windows_update = os.path.expandvars('%SystemRoot%\\SoftwareDistribution\\Download')
            self.clean_folder(windows_update)
            
            # 清理系统日志
            log_files = os.path.expandvars('%SystemRoot%\\Logs')
            self.clean_folder(log_files)
            
            # 清理Windows错误报告
            error_reports = os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\WER')
            self.clean_folder(error_reports)
            
            # 清理缩略图缓存
            thumbs_db = os.path.expanduser('~\\AppData\\Local\\Microsoft\\Windows\\Explorer')
            self.clean_folder(thumbs_db)
            
            # 清理预读取文件
            prefetch = os.path.expandvars('%SystemRoot%\\Prefetch')
            self.clean_folder(prefetch)
            
            # 清理字体缓存
            font_cache = os.path.expandvars('%SystemRoot%\\ServiceProfiles\\LocalService\\AppData\\Local\\FontCache')
            self.clean_folder(font_cache)
            
            # 清理安装缓存
            installer_cache = os.path.expandvars('%SystemRoot%\\Installer')
            self.clean_folder(installer_cache)
            
            # 清理系统补丁缓存
            patch_cache = os.path.expandvars('%SystemRoot%\\SoftwareDistribution\\Download')
            self.clean_folder(patch_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def is_admin(self):
        try:
            return os.getuid() == 0
        except AttributeError:
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    def request_admin_privileges(self):
        try:
            import ctypes, sys
            if not ctypes.windll.shell32.IsUserAnAdmin():
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
                sys.exit(0)
        except Exception as e:
            print(f"请求管理员权限时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass
    
    def get_folder_size(self, folder):
        total_size = 0
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    total_size += path.stat().st_size
        except:
            pass
        return total_size
    
    def _get_path_for_label(self, text):
        label_type = text.split('：')[0]
        paths = {
            '系统临时文件': tempfile.gettempdir(),
            '微信聊天记录': os.path.expanduser('~/Documents/WeChat Files'),
            'QQ聊天记录': os.path.expanduser('~/Documents/Tencent Files'),
            '浏览器缓存': [
                os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache'),
                os.path.expanduser('~/AppData/Local/Mozilla/Firefox/Profiles')
            ],
            'Windows更新缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download'),
            '系统日志文件': os.path.expandvars('%SystemRoot%/Logs'),
            '应用程序缓存': os.path.expanduser('~/AppData/Local/Temp'),
            'Windows错误报告': os.path.expanduser('~/AppData/Local/Microsoft/Windows/WER'),
            '缩略图缓存': os.path.expanduser('~/AppData/Local/Microsoft/Windows/Explorer'),
            '回收站': os.path.expanduser('~/$Recycle.Bin'),
            '预读取文件': os.path.expandvars('%SystemRoot%/Prefetch'),
            '字体缓存': os.path.expandvars('%SystemRoot%/ServiceProfiles/LocalService/AppData/Local/FontCache'),
            '安装缓存': os.path.expandvars('%SystemRoot%/Installer'),
            '系统补丁缓存': os.path.expandvars('%SystemRoot%/SoftwareDistribution/Download')
        }
        return paths.get(label_type)

    def clean_specific_folder(self, path):
        try:
            if not self.is_admin():
                self.request_admin_privileges()
                return
            
            if isinstance(path, list):
                for p in path:
                    self.clean_folder(p)
            elif path:
                if path.endswith('$Recycle.Bin'):
                    os.system('rd /s /q %systemdrive%\\$Recycle.bin')
                else:
                    self.clean_folder(path)
            
            # 显示清理完成提示
            QMessageBox.information(self, "清理完成", "所选垃圾文件已清理完成！")
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            QMessageBox.warning(self, "清理失败", f"清理时出错：{str(e)}")
            print(f"清理时出错：{str(e)}")

    def clean_junk(self):
        try:
            # 清理系统临时文件
            self.clean_folder(tempfile.gettempdir())
            
            # 清理微信聊天记录
            wechat_path = os.path.expanduser('~/Documents/WeChat Files')
            self.clean_folder(wechat_path)
            
            # 清理QQ聊天记录
            qq_path = os.path.expanduser('~/Documents/Tencent Files')
            self.clean_folder(qq_path)
            
            # 清理浏览器缓存
            chrome_cache = os.path.expanduser('~/AppData/Local/Google/Chrome/User Data/Default/Cache')
            edge_cache = os.path.expanduser('~/AppData/Local/Microsoft/Edge/User Data/Default/Cache')
            self.clean_folder(chrome_cache)
            self.clean_folder(edge_cache)
            
            # 清空回收站
            os.system('rd /s /q %systemdrive%\\$Recycle.bin')
            
            # 更新显示
            self.scan_junk()
        except Exception as e:
            print(f"清理时出错：{str(e)}")
    
    def clean_folder(self, folder):
        try:
            for path in Path(folder).rglob('*'):
                if path.is_file():
                    try:
                        path.unlink()
                    except:
                        pass
                elif path.is_dir():
                    try:
                        shutil.rmtree(path)
                    except:
                        pass
        except:
            pass