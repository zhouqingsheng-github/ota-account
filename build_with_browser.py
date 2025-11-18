#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本（包含浏览器）
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

# 设置 UTF-8 编码，避免 Windows 下的编码问题
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

def clean():
    """清理旧的打包文件"""
    print("清理旧文件...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  已删除: {dir_name}")
    
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"  已删除: {spec_file}")

def install_browser():
    """预先安装浏览器"""
    print("\n预先安装Playwright浏览器...")
    result = subprocess.run(
        [sys.executable, "-m", "playwright", "install", "chromium"],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        print("✅ 浏览器安装成功")
        return True
    else:
        print("❌ 浏览器安装失败")
        print(result.stderr)
        return False

def get_browser_path():
    """获取浏览器路径"""
    try:
        # 方法1: 从环境变量获取
        browsers_path = os.environ.get('PLAYWRIGHT_BROWSERS_PATH')
        if browsers_path and os.path.exists(browsers_path):
            print(f"\n从环境变量获取浏览器路径: {browsers_path}")
            return browsers_path
        
        # 方法2: 从 Playwright 获取
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            # 获取 chromium 可执行文件路径
            executable_path = Path(p.chromium.executable_path)
            # 浏览器根目录是 .../chromium-1234/chrome-win/chrome.exe
            # 我们需要 .../chromium-1234 这一层
            browser_path = executable_path.parent.parent
            
            # 如果路径包含 .local-browsers，则获取 .local-browsers 目录
            if '.local-browsers' in str(browser_path):
                parts = str(browser_path).split('.local-browsers')
                browser_root = parts[0] + '.local-browsers'
            else:
                # 否则获取所有浏览器的根目录
                browser_root = browser_path.parent
            
            print(f"\n浏览器根目录: {browser_root}")
            
            # 验证路径存在
            if os.path.exists(browser_root):
                return str(browser_root)
            else:
                print(f"警告: 浏览器路径不存在: {browser_root}")
                return None
                
    except Exception as e:
        print(f"获取浏览器路径失败: {e}")
        import traceback
        traceback.print_exc()
        return None

def build_with_browser():
    """打包（包含浏览器）"""
    print("\n开始打包（包含浏览器）...")
    
    # 获取浏览器路径
    browser_path = get_browser_path()
    if not browser_path:
        print("❌ 无法获取浏览器路径")
        return False
    
    # 验证浏览器路径存在
    if not os.path.exists(browser_path):
        print(f"❌ 浏览器路径不存在: {browser_path}")
        return False
    
    # 显示浏览器目录内容
    print(f"\n浏览器目录内容:")
    for item in os.listdir(browser_path):
        item_path = os.path.join(browser_path, item)
        if os.path.isdir(item_path):
            print(f"  📁 {item}")
        else:
            print(f"  📄 {item}")
    
    # 构建 --add-data 参数
    # 格式: 源路径;目标路径 (Windows) 或 源路径:目标路径 (macOS/Linux)
    add_data = f'{browser_path}{os.pathsep}playwright/driver/package/.local-browsers'
    print(f"\n--add-data 参数: {add_data}")
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=OTACredentialTool',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
        f'--add-data={add_data}',
        'ota_credential_tool.py'
    ]
    
    print(f"\n执行命令:")
    print(' '.join(cmd))
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ 打包成功！")
        
        # 根据平台显示不同的文件名
        if sys.platform == 'win32':
            app_name = "dist/OTACredentialTool.exe"
        elif sys.platform == 'darwin':
            app_name = "dist/OTACredentialTool.app"
        else:
            app_name = "dist/OTACredentialTool"
        
        print(f"\n应用程序位置: {app_name}")
        
        # 显示文件大小
        if sys.platform == 'darwin':
            # macOS .app 是目录
            app_path = Path("dist/OTACredentialTool.app")
            if app_path.exists():
                # 计算整个 .app 目录的大小
                total_size = sum(f.stat().st_size for f in app_path.rglob('*') if f.is_file())
                size_mb = total_size / (1024 * 1024)
                print(f"文件大小: {size_mb:.1f} MB")
        else:
            # Windows/Linux 是单个文件
            app_path = Path(app_name)
            if app_path.exists():
                size_mb = app_path.stat().st_size / (1024 * 1024)
                print(f"文件大小: {size_mb:.1f} MB")
        
        print("\n✨ 此版本包含浏览器，无需额外安装！")
        return True
    else:
        print("\n❌ 打包失败！")
        print("\n标准输出:")
        print(result.stdout)
        print("\n错误输出:")
        print(result.stderr)
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("OTA凭证工具 - 打包脚本（包含浏览器）")
    print("=" * 60)
    
    # 检查PyInstaller
    try:
        subprocess.run(['pyinstaller', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ 未安装 PyInstaller")
        print("\n请先安装: pip install pyinstaller")
        sys.exit(1)
    
    # 检查Playwright
    try:
        import playwright
    except ImportError:
        print("\n❌ 未安装 Playwright")
        print("\n请先安装: pip install playwright")
        sys.exit(1)
    
    clean()
    
    # 安装浏览器
    if not install_browser():
        print("\n⚠️  浏览器安装失败，但继续打包...")
    
    # 打包
    if build_with_browser():
        print("\n" + "=" * 60)
        print("打包完成！")
        print("=" * 60)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
