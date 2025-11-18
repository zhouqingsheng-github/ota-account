# 打包说明

## 环境准备

### 1. 安装依赖
```bash
cd ota-account
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器（可选）
```bash
playwright install chromium
```

## 打包步骤

### 方式1: 不包含浏览器（推荐，文件小）

```bash
python build.py
```

- 文件大小: 约50-80MB
- 首次运行需要下载浏览器（150MB）
- 适合网络分发

### 方式2: 包含浏览器（开箱即用）

```bash
# 先安装浏览器
playwright install chromium

# 打包（包含浏览器）
python build_with_browser.py
```

- 文件大小: 约200-250MB
- 无需额外下载，开箱即用
- 适合离线环境

### macOS 打包

打包完成后，应用程序位于：`dist/OTACredentialTool.app`

### Windows 打包

打包完成后，应用程序位于：`dist/OTACredentialTool.exe`

### Linux 打包

```bash
# 使用打包脚本
python build.py

# 或手动打包
pyinstaller --name="OTA凭证工具" --onefile --clean ota_credential_tool.py
```

打包完成后，应用程序位于：`dist/OTA凭证工具`

## 打包参数说明

- `--name`: 应用程序名称
- `--windowed`: 不显示控制台窗口（仅GUI）
- `--onefile`: 打包成单个文件
- `--clean`: 清理临时文件
- `--noconfirm`: 不询问确认
- `--icon`: 指定应用图标（可选）

## 分发说明

### macOS
1. 直接复制 `dist/OTA凭证工具.app` 给用户
2. 用户双击运行即可
3. 首次运行会提示安装浏览器（约150MB）

### Windows
1. 直接复制 `dist/OTA凭证工具.exe` 给用户
2. 用户双击运行即可
3. 首次运行会提示安装浏览器（约150MB）

### Linux
1. 复制 `dist/OTA凭证工具` 给用户
2. 添加执行权限：`chmod +x OTA凭证工具`
3. 运行：`./OTA凭证工具`

## 注意事项

1. **浏览器安装**：打包后的程序不包含Playwright浏览器，首次运行时会自动提示安装
2. **文件大小**：打包后的程序约50-100MB（不含浏览器）
3. **系统兼容性**：
   - macOS: 10.13+
   - Windows: 7/8/10/11
   - Linux: 主流发行版
4. **网络要求**：首次运行需要联网下载浏览器

## 故障排查

### 问题1: 打包失败
```bash
# 重新安装 PyInstaller
pip uninstall pyinstaller
pip install pyinstaller
```

### 问题2: 运行时缺少模块
```bash
# 检查依赖是否完整
pip install -r requirements.txt
```

### 问题3: macOS 提示"无法打开"
```bash
# 允许运行未签名的应用
xattr -cr "dist/OTA凭证工具.app"
```

### 问题4: Windows 杀毒软件误报
- 将程序添加到杀毒软件白名单
- 或使用代码签名证书签名程序

## 高级选项

### 添加应用图标

1. 准备图标文件：
   - macOS: `icon.icns`
   - Windows: `icon.ico`
   - Linux: `icon.png`

2. 打包时指定图标：
```bash
pyinstaller --name="OTA凭证工具" --windowed --onefile --icon=icon.ico ota_credential_tool.py
```

### 减小文件大小

```bash
# 使用 UPX 压缩
pyinstaller --name="OTA凭证工具" --windowed --onefile --upx-dir=/path/to/upx ota_credential_tool.py
```

### 包含额外文件

创建 `ota_credential_tool.spec` 文件，添加：
```python
datas=[('config.json', '.'), ('assets', 'assets')]
```

## 自动化打包

可以使用 GitHub Actions 或其他CI/CD工具自动打包多平台版本。

## 技术支持

如有问题，请检查：
1. Python版本：3.8+
2. PyInstaller版本：6.0+
3. 依赖包是否完整安装
