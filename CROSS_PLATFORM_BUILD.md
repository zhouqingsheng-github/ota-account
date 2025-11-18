# 跨平台打包指南

## 问题说明

在macOS上**无法直接打包**成Windows的.exe文件，因为：
- PyInstaller只能打包当前操作系统的可执行文件
- macOS → .app
- Windows → .exe
- Linux → 二进制文件

## 解决方案

### 方案1: GitHub Actions（推荐，免费）

#### 步骤：

1. **将代码推送到GitHub**
```bash
git add .
git commit -m "Add OTA credential tool"
git push
```

2. **创建Release触发打包**
```bash
# 打标签
git tag v1.0.0
git push origin v1.0.0
```

3. **下载打包好的文件**
- 进入GitHub仓库的 Actions 页面
- 等待打包完成（约5-10分钟）
- 下载三个平台的文件：
  - `OTA凭证工具-Windows.exe`
  - `OTA凭证工具-macOS.app`
  - `OTA凭证工具-Linux`

#### 优点：
✅ 完全免费
✅ 自动化打包
✅ 同时生成三个平台版本
✅ 无需本地环境

---

### 方案2: 使用Windows虚拟机

#### 在macOS上安装Windows虚拟机：

**选项A: Parallels Desktop（付费，推荐）**
```bash
# 1. 安装Parallels Desktop
# 2. 创建Windows 11虚拟机
# 3. 在虚拟机中安装Python和依赖
# 4. 运行打包命令
```

**选项B: VirtualBox（免费）**
```bash
# 1. 安装VirtualBox
brew install --cask virtualbox

# 2. 下载Windows 11 ISO
# 3. 创建虚拟机
# 4. 在虚拟机中打包
```

#### 在虚拟机中打包：
```bash
# 安装Python 3.11
# 安装依赖
pip install -r requirements.txt
pip install pyinstaller

# 打包
python build.py
```

---

### 方案3: 使用Docker + Wine（复杂）

```dockerfile
# Dockerfile
FROM tobix/pywine:3.11

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install pyinstaller

COPY . .
RUN pyinstaller --name="OTA凭证工具" --windowed --onefile ota_credential_tool.py
```

```bash
# 构建并运行
docker build -t ota-builder .
docker run -v $(pwd)/dist:/app/dist ota-builder
```

---

### 方案4: 租用Windows云服务器

**选项A: 阿里云/腾讯云**
- 按小时计费
- 远程桌面连接
- 打包完成后释放

**选项B: AWS EC2**
- 免费套餐
- Windows Server
- 远程打包

---

### 方案5: 找Windows电脑帮忙

最简单的方式：
1. 将代码复制到U盘
2. 在Windows电脑上打包
3. 复制回来

---

## 推荐方案对比

| 方案 | 成本 | 难度 | 时间 | 推荐度 |
|------|------|------|------|--------|
| GitHub Actions | 免费 | ⭐ | 10分钟 | ⭐⭐⭐⭐⭐ |
| Parallels Desktop | ¥698/年 | ⭐⭐ | 1小时 | ⭐⭐⭐⭐ |
| VirtualBox | 免费 | ⭐⭐⭐ | 2小时 | ⭐⭐⭐ |
| Docker + Wine | 免费 | ⭐⭐⭐⭐ | 3小时 | ⭐⭐ |
| 云服务器 | ¥10-50 | ⭐⭐ | 30分钟 | ⭐⭐⭐ |
| 借Windows电脑 | 免费 | ⭐ | 20分钟 | ⭐⭐⭐⭐ |

---

## 最佳实践

### 如果你有GitHub账号（推荐）

1. 创建GitHub仓库
2. 推送代码
3. 使用GitHub Actions自动打包
4. 下载所有平台的版本

### 如果没有GitHub账号

1. 找一台Windows电脑（朋友/公司/网吧）
2. 安装Python和依赖
3. 运行 `python build.py`
4. 复制生成的.exe文件

---

## GitHub Actions 使用教程

### 1. 创建GitHub仓库
```bash
# 初始化git（如果还没有）
cd python-tool
git init
git add .
git commit -m "Initial commit"

# 创建GitHub仓库并推送
git remote add origin https://github.com/你的用户名/ota-tool.git
git push -u origin main
```

### 2. 添加工作流文件
已经创建好了：`.github/workflows/build.yml`

### 3. 触发打包
```bash
# 方式1: 创建标签
git tag v1.0.0
git push origin v1.0.0

# 方式2: 手动触发
# 在GitHub网页上：Actions → Build OTA Tool → Run workflow
```

### 4. 下载文件
- 进入 Actions 页面
- 点击最新的工作流运行
- 下载 Artifacts 中的文件

---

## 常见问题

**Q: 为什么macOS不能打包Windows程序？**
A: 因为可执行文件格式不同，需要在目标平台上打包。

**Q: 有没有在线打包服务？**
A: GitHub Actions就是免费的在线打包服务。

**Q: 打包后的程序能在所有Windows版本运行吗？**
A: 支持Windows 7/8/10/11，但需要安装对应的运行时。

**Q: 可以用Wine在macOS上运行Windows程序吗？**
A: 可以运行，但打包仍需要Windows环境。

---

## 总结

**最简单的方法**：使用GitHub Actions，完全免费且自动化。

如果不想用GitHub，就找一台Windows电脑打包一次即可。
