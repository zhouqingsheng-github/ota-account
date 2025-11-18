# GitHub Actions 自动打包教程

## 📋 前置条件

1. 有GitHub账号（没有的话去 https://github.com 注册）
2. 本地安装了Git

## 🚀 快速开始

### 步骤1: 初始化Git仓库

在 `python-tool` 目录下执行：

```bash
# 初始化Git仓库
git init

# 添加所有文件
git add .

# 提交
git commit -m "Initial commit: OTA凭证获取工具"
```

### 步骤2: 在GitHub创建仓库

1. 访问 https://github.com/new
2. 填写仓库信息：
   - Repository name: `ota-credential-tool`（或其他名字）
   - Description: `OTA平台凭证获取工具`
   - 选择 `Public` 或 `Private`（都可以用Actions）
3. **不要**勾选 "Add a README file"
4. 点击 "Create repository"

### 步骤3: 推送代码到GitHub

复制GitHub页面上的命令，或执行：

```bash
# 添加远程仓库（替换成你的用户名和仓库名）
git remote add origin https://github.com/你的用户名/ota-credential-tool.git

# 推送代码
git branch -M main
git push -u origin main
```

### 步骤4: 触发自动打包

有两种方式触发打包：

#### 方式A: 创建Release标签（推荐）

```bash
# 创建标签
git tag v1.0.0

# 推送标签
git push origin v1.0.0
```

#### 方式B: 手动触发

1. 进入GitHub仓库页面
2. 点击 `Actions` 标签
3. 选择 `Build OTA Tool` 工作流
4. 点击右侧 `Run workflow` 按钮
5. 点击绿色的 `Run workflow` 确认

### 步骤5: 等待打包完成

1. 在 `Actions` 页面可以看到打包进度
2. 大约需要 5-10 分钟
3. 三个平台会并行打包：
   - ✅ Windows (.exe)
   - ✅ macOS (.app)
   - ✅ Linux (二进制)

### 步骤6: 下载打包好的文件

打包完成后：

1. 点击完成的工作流运行
2. 滚动到底部的 `Artifacts` 区域
3. 下载三个文件：
   - `OTA凭证工具-Windows` → 解压得到 .exe
   - `OTA凭证工具-macOS` → 解压得到 .app
   - `OTA凭证工具-Linux` → 解压得到二进制文件

## 📦 文件说明

下载后的文件：

### Windows版本
- 文件名: `OTA凭证工具.exe`
- 大小: 约 50-80MB
- 系统要求: Windows 7/8/10/11
- 使用: 双击运行

### macOS版本
- 文件名: `OTA凭证工具.app`
- 大小: 约 50-80MB
- 系统要求: macOS 10.13+
- 使用: 双击运行
- 注意: 首次运行可能需要在"系统偏好设置 → 安全性与隐私"中允许

### Linux版本
- 文件名: `OTA凭证工具`
- 大小: 约 50-80MB
- 系统要求: 主流Linux发行版
- 使用: 
  ```bash
  chmod +x OTA凭证工具
  ./OTA凭证工具
  ```

## 🔄 更新版本

当你修改代码后，重新打包：

```bash
# 提交修改
git add .
git commit -m "更新说明"
git push

# 创建新版本标签
git tag v1.0.1
git push origin v1.0.1
```

## ❓ 常见问题

### Q1: Actions运行失败怎么办？

**A:** 点击失败的工作流，查看错误日志。常见原因：
- 依赖安装失败 → 检查 requirements.txt
- 代码语法错误 → 本地先测试
- 网络问题 → 重新运行工作流

### Q2: 下载的文件在哪里？

**A:** 
1. GitHub Actions页面
2. 点击完成的工作流
3. 滚动到底部 `Artifacts` 区域
4. 点击下载

### Q3: 可以只打包Windows版本吗？

**A:** 可以，修改 `.github/workflows/build.yml`，删除不需要的job。

### Q4: 打包需要付费吗？

**A:** 
- Public仓库：完全免费，无限制
- Private仓库：每月2000分钟免费额度（足够用）

### Q5: 如何分发给用户？

**A:** 
1. 在GitHub创建Release
2. 上传打包好的文件
3. 分享Release链接给用户

创建Release：
```bash
# 在GitHub仓库页面
1. 点击右侧 "Releases"
2. 点击 "Create a new release"
3. 选择标签 v1.0.0
4. 填写标题和说明
5. 上传打包好的文件
6. 点击 "Publish release"
```

## 🎯 完整流程示例

```bash
# 1. 初始化
cd python-tool
git init
git add .
git commit -m "Initial commit"

# 2. 推送到GitHub
git remote add origin https://github.com/你的用户名/ota-credential-tool.git
git push -u origin main

# 3. 触发打包
git tag v1.0.0
git push origin v1.0.0

# 4. 等待5-10分钟

# 5. 在GitHub Actions页面下载文件
```

## 📝 工作流配置说明

`.github/workflows/build.yml` 文件已经配置好了：

- **触发条件**: 
  - 推送标签（v开头）
  - 手动触发
  
- **打包平台**:
  - Windows (windows-latest)
  - macOS (macos-latest)
  - Linux (ubuntu-latest)

- **Python版本**: 3.11

- **打包参数**:
  - `--windowed`: 无控制台窗口
  - `--onefile`: 单文件
  - `--clean`: 清理临时文件

## 🔧 自定义配置

如果需要修改打包参数，编辑 `.github/workflows/build.yml`：

```yaml
# 例如：添加图标
- name: Build Windows EXE
  run: |
    cd python-tool
    pyinstaller --name="OTA凭证工具" --windowed --onefile --icon=icon.ico --clean ota_credential_tool.py
```

## 📞 需要帮助？

如果遇到问题：
1. 查看GitHub Actions的运行日志
2. 检查本地代码是否能正常运行
3. 确认所有文件都已提交到Git

---

**祝你打包顺利！** 🎉
