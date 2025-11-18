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
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser_path = Path(p.chromium.executable_path).parent.parent
            print(f"\n浏览器路径: {browser_path}")
            return str(browser_path)
    except Exception as e:
        print(f"获取浏览器路径失败: {e}")
        return None

def build_with_browser():
    """打包（包含浏览器）"""
    print("\n开始打包（包含浏览器）...")
    
    # 获取浏览器路径
    browser_path = get_browser_path()
    if not browser_path:
        print("❌ 无法获取浏览器路径")
        return False
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=OTACredentialTool',
        '--windowed',
        '--onefile',
        '--clean',
        '--noconfirm',
        f'--add-data={browser_path}{os.pathsep}playwright/driver/package/.local-browsers',
        'ota_credential_tool.py'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ 打包成功！")
        print(f"\n应用程序位置: dist/OTACredentialTool.exe")
        
        # 显示文件大小
        exe_path = Path("dist/OTACredentialTool.exe")
        if exe_path.exists():
            size_mb = exe_path.stat().st_size / (1024 * 1024)
            print(f"文件大小: {size_mb:.1f} MB")
        
        print("\n✨ 此版本包含浏览器，无需额外安装！")
        return True
    else:
        print("\n❌ 打包失败！")
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
