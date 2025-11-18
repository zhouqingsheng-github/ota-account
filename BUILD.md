# 打包说明

## ⚠️ 重要提示

**打包后的 exe 无法执行 `playwright install chromium`！**

原因：
- 客户端没有 Python 环境
- exe 是只读的，无法写入文件
- 必须在打包前把浏览器打包进去

**给客户分发时，请使用"方式2: 包含浏览器"！**

详细说明请查看 [FAQ.md](FAQ.md)

---

## 环境准备

### 1. 安装依赖
```bash
cd ota-account
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器（必须！）
```bash
playwright install chromium
```

## 打包步骤

### 方式1: 不包含浏览器（仅供开发测试）

```bash
python build.py
```

- 文件大小: 约50-80MB
- ❌ **不适合给客户**
- ❌ 客户运行时会报错
- ✅ 仅用于开发快速测试

### 方式2: 包含浏览器（推荐给客户）⭐

```bash
# 1. 先安装浏览器（如果还没安装）
playwright install chromium

# 2. 打包（会自动包含浏览器）
python build_with_browser.py
```

- 文件大小: 约200-250MB
- ✅ **推荐给客户使用**
- ✅ 开箱即用，无需安装
- ✅ 无需 Python 环境
- ✅ 无需网络连接

## 打包后的文件位置

### Windows
```
dist/OTACredentialTool.exe
```

### macOS
```
dist/OTACredentialTool.app
```

### Linux
```
dist/OTACredentialTool
```

## 分发给客户

### 推荐流程

1. **打包完整版本**：
```bash
python build_with_browser.py
```

2. **测试**：
- 在干净的虚拟机上测试
- 确保没有 Python 环境
- 确保能正常运行

3. **分发**：
- 直接发送 exe/app 文件
- 或上传到云存储提供下载链接

### 使用说明（给客户）

**Windows**：
1. 双击 `OTACredentialTool.exe`
2. 选择平台、输入账号密码
3. 点击"获取凭证"

**macOS**：
1. 双击 `OTACredentialTool.app`
2. 如果提示"无法打开"，运行：
```bash
xattr -cr OTACredentialTool.app
```
3. 再次双击运行

**Linux**：
1. 添加执行权限：
```bash
chmod +x OTACredentialTool
```
2. 运行：
```bash
./OTACredentialTool
```

## 故障排查

### 问题1: 打包失败

```bash
# 重新安装依赖
pip uninstall pyinstaller playwright
pip install pyinstaller playwright

# 重新安装浏览器
playwright install chromium

# 重新打包
python build_with_browser.py
```

### 问题2: 打包后提示"浏览器缺失"

**原因**：使用了 `build.py` 而不是 `build_with_browser.py`

**解决**：
```bash
python build_with_browser.py
```

### 问题3: 客户运行时报错

**检查清单**：
- ✅ 是否使用 `build_with_browser.py` 打包？
- ✅ 打包前是否安装了浏览器？
- ✅ 打包日志是否显示浏览器路径？
- ✅ 文件大小是否约 200-250MB？

如果文件只有 50-80MB，说明没有包含浏览器！

## 高级选项

### 添加应用图标

1. 准备图标文件：
   - Windows: `icon.ico`
   - macOS: `icon.icns`

2. 修改打包脚本，添加：
```python
'--icon=icon.ico',
```

### 使用 UPX 压缩

可以减少 20-30% 文件大小：

```bash
# 安装 UPX
# macOS
brew install upx

# Windows
# 从 https://upx.github.io/ 下载

# 打包时使用
pyinstaller --upx-dir=/path/to/upx ...
```

## 技术支持

遇到问题？查看：
1. [FAQ.md](FAQ.md) - 常见问题解答
2. [BROWSER_PACKAGING.md](BROWSER_PACKAGING.md) - 浏览器打包详解

## 总结

**记住这些要点**：
1. ❌ 打包后的 exe **不能**自动下载浏览器
2. ✅ 必须使用 `build_with_browser.py` 打包
3. ✅ 打包前必须先安装浏览器
4. ✅ 给客户的版本必须包含浏览器
5. ✅ 文件大小应该是 200-250MB（包含浏览器）
