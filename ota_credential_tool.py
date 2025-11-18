#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
OTA凭证获取工具
支持美团、飞猪、携程平台的登录凭证获取
"""

import sys
import json
import subprocess
import os
from typing import Optional
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QTextEdit, QMessageBox,
    QProgressDialog
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page, Error


class BrowserInstallWorker(QThread):
    """浏览器安装工作线程"""
    finished = pyqtSignal(bool, str)  # 成功/失败, 消息
    progress = pyqtSignal(str)  # 进度信息
    
    def __init__(self):
        super().__init__()
    
    def run(self):
        """执行浏览器安装"""
        try:
            self.progress.emit("正在安装Chromium浏览器...")
            
            # 执行 playwright install chromium
            process = subprocess.Popen(
                [sys.executable, "-m", "playwright", "install", "chromium"],
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )
            
            # 实时读取输出
            for line in process.stdout:
                self.progress.emit(line.strip())
            
            process.wait()
            
            if process.returncode == 0:
                self.finished.emit(True, "浏览器安装成功！")
            else:
                self.finished.emit(False, "浏览器安装失败")
                
        except Exception as e:
            self.finished.emit(False, f"安装出错: {str(e)}")


class LoginWorker(QThread):
    """登录工作线程"""
    finished = pyqtSignal(bool, str)  # 成功/失败, 凭证/错误信息
    browser_missing = pyqtSignal()  # 浏览器缺失信号
    
    def __init__(self, platform: str, username: str, password: str):
        super().__init__()
        self.platform = platform
        self.username = username
        self.password = password
    
    def run(self):
        """执行登录"""
        try:
            credential = self.login()
            self.finished.emit(True, credential)
        except Error as e:
            # 检查是否是浏览器缺失错误
            if "Executable doesn't exist" in str(e) or "Looks like Playwright was just installed" in str(e):
                self.browser_missing.emit()
            else:
                self.finished.emit(False, str(e))
        except Exception as e:
            self.finished.emit(False, str(e))
    
    def login(self) -> str:
        """执行登录并获取凭证"""
        with sync_playwright() as p:
            # 启动浏览器，添加参数避免被检测
            browser = p.chromium.launch(
                headless=False,
                args=[
                    '--disable-blink-features=AutomationControlled',
                    '--disable-dev-shm-usage',
                    '--no-sandbox'
                ]
            )
            
            # 创建上下文，模拟真实浏览器
            context = browser.new_context(
                viewport={'width': 1920, 'height': 1080},
                user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                locale='zh-CN',
                timezone_id='Asia/Shanghai'
            )
            
            page = context.new_page()
            
            # 隐藏webdriver特征
            page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined
                });
                
                window.navigator.chrome = {
                    runtime: {}
                };
                
                Object.defineProperty(navigator, 'plugins', {
                    get: () => [1, 2, 3, 4, 5]
                });
                
                Object.defineProperty(navigator, 'languages', {
                    get: () => ['zh-CN', 'zh', 'en']
                });
            """)
            
            try:
                if self.platform == "美团":
                    self._login_meituan(page)
                elif self.platform == "飞猪":
                    self._login_fliggy(page)
                elif self.platform == "携程":
                    self._login_ctrip(page)
                else:
                    raise ValueError(f"不支持的平台: {self.platform}")
                
                # 最终验证登录状态
                page.wait_for_timeout(2000)
                current_url = page.url
                
                # 根据平台验证登录状态
                if self.platform == "美团" and "ebooking" not in current_url:
                    raise Exception("美团登录验证失败: 未在后台页面")
                elif self.platform == "飞猪" and ("login" in current_url or "ebooking" not in current_url):
                    raise Exception("飞猪登录验证失败: 未在后台页面")
                elif self.platform == "携程" and "login" in current_url:
                    raise Exception("携程登录验证失败: 未在后台页面")
                
                # 获取凭证
                credential = self._get_credential(context)
                return credential
                
            finally:
                page.close()
                context.close()
                browser.close()
    
    def _login_meituan(self, page: Page):
        """美团登录"""
        # 访问登录页面
        page.goto("https://me.meituan.com/login/index.html")
        page.wait_for_load_state("networkidle")
        
        # 等待登录 iframe
        page.wait_for_selector("iframe.login-iframe", timeout=15000)
        frame = page.query_selector("iframe.login-iframe").content_frame()
        
        # 填写账号密码
        frame.fill("input#login", self.username)
        frame.fill("input#password", self.password)
        
        # 勾选协议
        frame.evaluate("""() => {
            const checkbox = document.querySelector('input#checkbox');
            if (checkbox && !checkbox.checked) {
                checkbox.click();
            }
        }""")
        
        # 点击登录
        frame.click("button.ep-login_btn")
        
        # 等待登录成功
        try:
            page.wait_for_url("**/ebooking/**", timeout=120000)
        except Exception as e:
            # 检查是否有错误提示
            error_msg = self._check_login_error(page, frame)
            if error_msg:
                raise Exception(f"美团登录失败: {error_msg}")
            raise Exception(f"美团登录超时或失败: {str(e)}")
        
        # 验证是否真的登录成功
        if "ebooking" not in page.url:
            raise Exception("美团登录失败: 未能跳转到后台页面")

    def _login_fliggy(self, page: Page):
        """飞猪登录"""
        # 访问登录页面
        page.goto("https://hotel.fliggy.com/ebooking/login.htm#/")
        page.wait_for_load_state("networkidle")
        
        # 检查是否已登录
        if "hotel.fliggy.com/ebooking/login.htm" not in page.url:
            return
        
        # 输入账号
        page.wait_for_selector("input[name='username']", timeout=15000)
        page.fill("input[name='username']", self.username)
        page.wait_for_timeout(500)
        
        # 点击下一步
        page.click("button.login-button")
        page.wait_for_timeout(2000)
        
        # 等待 iframe 并输入密码
        page.wait_for_selector("#alibaba-login-box", timeout=15000)
        login_frame = page.frame_locator("#alibaba-login-box")
        
        login_frame.locator("#fm-login-password").wait_for(timeout=10000)
        login_frame.locator("#fm-login-password").fill(self.password)
        page.wait_for_timeout(500)
        
        # 点击登录
        login_frame.locator("button.fm-submit.password-login").click()
        
        # 等待登录成功
        try:
            page.wait_for_url("**/hotel.fliggy.com/ebooking/**", timeout=120000)
        except Exception as e:
            raise Exception(f"飞猪登录超时或失败: {str(e)}")
        
        # 验证是否真的登录成功
        if "hotel.fliggy.com/ebooking" not in page.url or "login" in page.url:
            raise Exception("飞猪登录失败: 未能跳转到后台页面")
    
    def _login_ctrip(self, page: Page):
        """携程登录"""
        # 访问登录页面
        page.goto("https://ebooking.ctrip.com/login/index")
        page.wait_for_load_state("networkidle")
        
        # 检查是否已登录
        if "login" not in page.url:
            return
        
        # 等待登录表单
        page.wait_for_selector("input[name='username-input']", timeout=10000)
        
        # 填写账号密码
        page.fill("input[name='username-input']", self.username)
        page.fill("input[name='password-input']", self.password)
        page.wait_for_timeout(500)
        
        # 点击登录
        page.click("button#hotel-login-box-button")
        page.wait_for_timeout(3000)
        
        # 等待登录结果（最多120秒，给用户时间处理验证码）
        max_wait = 120
        for i in range(max_wait):
            page.wait_for_timeout(1000)
            current_url = page.url
            
            # 检查是否登录成功
            if "login" not in current_url and "ebooking.ctrip.com" in current_url:
                return
            
            # 检查是否有错误提示
            error_elem = page.query_selector(".error-message, .login-error, [class*='error']")
            if error_elem and error_elem.is_visible():
                error_text = error_elem.text_content()
                if error_text and error_text.strip():
                    raise Exception(f"携程登录失败: {error_text}")
        
        # 超时后再次检查
        if "login" in page.url:
            raise Exception("携程登录超时: 请检查账号密码或手动完成验证")
    
    def _check_login_error(self, page: Page, frame=None) -> str:
        """检查登录错误信息"""
        try:
            # 在iframe中查找错误
            if frame:
                error_selectors = [
                    ".error-message",
                    ".login-error",
                    "[class*='error']",
                    ".tip-error"
                ]
                for selector in error_selectors:
                    error_elem = frame.query_selector(selector)
                    if error_elem and error_elem.is_visible():
                        error_text = error_elem.text_content()
                        if error_text and error_text.strip():
                            return error_text.strip()
            
            # 在主页面查找错误
            error_selectors = [
                ".error-message",
                ".login-error",
                "[class*='error']"
            ]
            for selector in error_selectors:
                error_elem = page.query_selector(selector)
                if error_elem and error_elem.is_visible():
                    error_text = error_elem.text_content()
                    if error_text and error_text.strip():
                        return error_text.strip()
        except:
            pass
        return ""
    
    def _get_credential(self, context: BrowserContext) -> str:
        """获取浏览器上下文凭证"""
        # 获取存储状态
        storage_state = context.storage_state()
        
        # 检查是否有有效的cookies
        if not storage_state.get('cookies') or len(storage_state['cookies']) == 0:
            raise Exception("获取凭证失败: 未找到有效的Cookie信息")
        
        # 转换为JSON字符串
        credential_json = json.dumps(storage_state, ensure_ascii=False, indent=2)
        
        return credential_json


class OTACredentialTool(QMainWindow):
    """OTA凭证获取工具主窗口"""
    
    def __init__(self):
        super().__init__()
        self.worker: Optional[LoginWorker] = None
        self.install_worker: Optional[BrowserInstallWorker] = None
        self.progress_dialog: Optional[QProgressDialog] = None
        self.browser_checked = False  # 标记是否已检查过浏览器
        self.init_ui()
        # 不在启动时检查，改为点击获取凭证时检查
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("OTA凭证获取工具")
        self.setMinimumSize(800, 600)
        
        # 中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 主布局
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # 标题
        title = QLabel("OTA平台凭证获取工具")
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        
        # 平台选择
        platform_layout = QHBoxLayout()
        platform_label = QLabel("OTA渠道:")
        platform_label.setFixedWidth(80)
        self.platform_combo = QComboBox()
        self.platform_combo.addItems(["美团", "飞猪", "携程"])
        platform_layout.addWidget(platform_label)
        platform_layout.addWidget(self.platform_combo)
        layout.addLayout(platform_layout)
        
        # 账号输入
        username_layout = QHBoxLayout()
        username_label = QLabel("账号:")
        username_label.setFixedWidth(80)
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("请输入账号")
        username_layout.addWidget(username_label)
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # 密码输入
        password_layout = QHBoxLayout()
        password_label = QLabel("密码:")
        password_label.setFixedWidth(80)
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(password_label)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # 获取凭证按钮
        self.get_credential_btn = QPushButton("获取凭证")
        self.get_credential_btn.setStyleSheet("""
            QPushButton {
                background-color: #1890ff;
                color: white;
                border: none;
                padding: 10px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #40a9ff;
            }
            QPushButton:disabled {
                background-color: #d9d9d9;
            }
        """)
        self.get_credential_btn.clicked.connect(self.get_credential)
        layout.addWidget(self.get_credential_btn)
        
        # 凭证显示区域
        credential_label = QLabel("凭证内容:")
        layout.addWidget(credential_label)
        
        self.credential_text = QTextEdit()
        self.credential_text.setReadOnly(True)
        self.credential_text.setPlaceholderText("凭证将在这里显示...")
        layout.addWidget(self.credential_text)
        
        # 复制按钮
        self.copy_btn = QPushButton("复制凭证")
        self.copy_btn.setEnabled(False)
        self.copy_btn.setStyleSheet("""
            QPushButton {
                background-color: #52c41a;
                color: white;
                border: none;
                padding: 8px;
                font-size: 14px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #73d13d;
            }
            QPushButton:disabled {
                background-color: #d9d9d9;
            }
        """)
        self.copy_btn.clicked.connect(self.copy_credential)
        layout.addWidget(self.copy_btn)
    

    
    def install_browser(self):
        """安装浏览器"""
        # 创建进度对话框
        self.progress_dialog = QProgressDialog("正在安装浏览器，请稍候...", None, 0, 0, self)
        self.progress_dialog.setWindowTitle("安装中")
        self.progress_dialog.setWindowModality(Qt.WindowModality.WindowModal)
        self.progress_dialog.setMinimumDuration(0)
        self.progress_dialog.setFixedSize(350, 100)  # 固定大小
        self.progress_dialog.setCancelButton(None)  # 禁用取消按钮
        self.progress_dialog.show()
        
        # 创建安装工作线程
        self.install_worker = BrowserInstallWorker()
        self.install_worker.progress.connect(self.on_install_progress)
        self.install_worker.finished.connect(self.on_install_finished)
        self.install_worker.start()
    
    def on_install_progress(self, message: str):
        """安装进度更新"""
        if self.progress_dialog and message:
            # 只显示关键信息，过滤掉过长的输出
            if "Downloading" in message or "下载" in message:
                self.progress_dialog.setLabelText("正在下载浏览器...")
            elif "Installing" in message or "安装" in message:
                self.progress_dialog.setLabelText("正在安装浏览器...")
            elif "%" in message:
                # 显示百分比进度
                self.progress_dialog.setLabelText(f"正在下载: {message}")
    
    def on_install_finished(self, success: bool, message: str):
        """安装完成"""
        if self.progress_dialog:
            self.progress_dialog.close()
            self.progress_dialog = None
        
        if success:
            self.browser_checked = False  # 重置标记，下次点击时会重新检查
            QMessageBox.information(self, "成功", f"{message}\n\n现在可以点击\"获取凭证\"按钮了。")
        else:
            QMessageBox.critical(self, "错误", message)
    
    def get_credential(self):
        """获取凭证"""
        # 验证输入
        platform = self.platform_combo.currentText()
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        
        if not username:
            QMessageBox.warning(self, "警告", "请输入账号")
            return
        
        if not password:
            QMessageBox.warning(self, "警告", "请输入密码")
            return
        
        # 首次使用时检查浏览器
        if not self.browser_checked:
            self.browser_checked = True
            if not self.check_browser_installed():
                return  # 用户取消安装，不继续
        
        # 禁用按钮
        self.get_credential_btn.setEnabled(False)
        self.get_credential_btn.setText("登录中...")
        self.credential_text.clear()
        self.copy_btn.setEnabled(False)
        
        # 创建工作线程
        self.worker = LoginWorker(platform, username, password)
        self.worker.finished.connect(self.on_login_finished)
        self.worker.browser_missing.connect(self.on_browser_missing)
        self.worker.start()
    
    def check_browser_installed(self) -> bool:
        """检查浏览器是否已安装，返回True表示已安装或用户选择安装"""
        try:
            with sync_playwright() as p:
                browser_path = p.chromium.executable_path
                if os.path.exists(browser_path):
                    return True
                raise FileNotFoundError("浏览器不存在")
        except Exception as e:
            error_msg = str(e)
            if "Executable doesn't exist" in error_msg or "Looks like Playwright" in error_msg:
                reply = QMessageBox.question(
                    self,
                    "浏览器未安装",
                    "检测到Playwright浏览器未安装，是否现在安装？\n\n"
                    "安装大约需要下载150MB，请确保网络连接正常。",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if reply == QMessageBox.StandardButton.Yes:
                    self.install_browser()
                    return False  # 正在安装，本次不执行登录
                else:
                    return False  # 用户取消
            return True  # 其他错误，假设浏览器存在
    
    def on_browser_missing(self):
        """浏览器缺失处理"""
        self.get_credential_btn.setEnabled(True)
        self.get_credential_btn.setText("获取凭证")
        
        reply = QMessageBox.question(
            self,
            "浏览器未安装",
            "检测到Playwright浏览器未安装，是否现在安装？\n\n"
            "安装大约需要下载150MB，请确保网络连接正常。",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            self.install_browser()
    
    def on_login_finished(self, success: bool, result: str):
        """登录完成回调"""
        self.get_credential_btn.setEnabled(True)
        self.get_credential_btn.setText("获取凭证")
        
        if success:
            self.credential_text.setPlainText(result)
            self.copy_btn.setEnabled(True)
            QMessageBox.information(self, "成功", "凭证获取成功！")
        else:
            QMessageBox.critical(self, "错误", f"登录失败：{result}")
    
    def copy_credential(self):
        """复制凭证到剪贴板"""
        credential = self.credential_text.toPlainText()
        if credential:
            clipboard = QApplication.clipboard()
            clipboard.setText(credential)
            QMessageBox.information(self, "成功", "凭证已复制到剪贴板")


def main():
    """主函数"""
    app = QApplication(sys.argv)
    window = OTACredentialTool()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
