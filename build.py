#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
打包脚本
"""

import os
import sys
import subprocess
import shutil

def clean():
    """清理旧的打包文件"""
    print("清理旧文件...")
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"  已删除: {dir_name}")
    
    # 删除 .spec 文件
    spec_files = [f for f in os.listdir('.') if f.endswith('.spec')]
    for spec_file in spec_files:
        os.remove(spec_file)
        print(f"  已删除: {spec_file}")

def build():
    """执行打包"""
    print("\n开始打包...")
    
    # PyInstaller 命令
    cmd = [
        'pyinstaller',
        '--name=OTA凭证工具',
        '--windowed',  # 不显示控制台窗口
        '--onefile',   # 打包成单个文件
        '--clean',
        '--noconfirm',
        'ota_credential_tool.py'
    ]
    
    print(f"执行命令: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    if result.returncode == 0:
        print("\n✅ 打包成功！")
        print(f"\n应用程序位置: dist/OTA凭证工具.app")
        print("\n使用说明:")
        print("1. 双击运行 dist/OTA凭证工具.app")
        print("2. 首次运行会提示安装浏览器，点击确定即可")
        print("3. 如需分发给他人，直接复制 .app 文件即可")
    else:
        print("\n❌ 打包失败！")
        print(result.stderr)
        sys.exit(1)

def main():
    """主函数"""
    print("=" * 60)
    print("OTA凭证工具 - 打包脚本")
    print("=" * 60)
    
    # 检查是否安装了 PyInstaller
    try:
        subprocess.run(['pyinstaller', '--version'], 
                      capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("\n❌ 未安装 PyInstaller")
        print("\n请先安装: pip install pyinstaller")
        sys.exit(1)
    
    clean()
    build()
    
    print("\n" + "=" * 60)
    print("打包完成！")
    print("=" * 60)

if __name__ == '__main__':
    main()
