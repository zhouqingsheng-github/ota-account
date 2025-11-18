# GitHub Actions 自动打包说明

## 概述

使用 GitHub Actions 在云端自动打包 Windows exe，无需本地 Windows 环境。

## 使用方法

### 方式1: 自动触发（推荐）

每次推送代码到 `main` 或 `master` 分支时，自动触发打包：

```bash
git add .
git commit -m "更新代码"
git push origin main
```

### 方式2: 手动触发

1. 打开 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 选择 **Build Windows EXE** workflow
4. 点击右侧 **Run workflow** 按钮
5. 选择分支，点击 **Run workflow**

## 下载打包好的文件

### 从 Actions 下载

1. 打开 GitHub 仓库页面
2. 点击 **Actions** 标签
3. 点击最新的成功运行（绿色✓）
4. 在 **Artifacts** 区域找到 `OTA-Credential-Tool-Windows-xxx`
5. 点击下载（zip 格式）
6. 解压得到 `OTACredentialTool.exe`

### 从 Release 下载（如果创建了 tag）

```bash
# 创建 tag 并推送
git tag v1.0.0
git push origin v1.0.0
```

然后在 GitHub 的 **Releases** 页面下载。

## 工作流程

1. **检出代码** - 从仓库拉取最新代码
2. **设置 Python** - 安装 Python 3.11
3. **安装依赖** - 安装 requirements.txt 中的包
4. **安装浏览器** - 下载 Chromium 浏览器
5. **打包** - 运行 `build_with_browser.py`
6. **检查结果** - 验证 exe 文件并显示大小
7. **上传** - 将 exe 上传为 artifact

## 预期结果

- **文件名**: `OTACredentialTool.exe`
- **文件大小**: 约 200-250 MB
- **包含内容**: 程序 + Chromium 浏览器
- **运行要求**: 无需 Python，无需网络，开箱即用

## 构建时间

- 首次构建: 约 5-10 分钟
- 后续构建: 约 3-5 分钟（有缓存）

## 故障排查

### 问题1: 构建失败

查看 Actions 日志：
1. 点击失败的运行（红色 ✗）
2. 点击 **build-windows** job
3. 查看具体哪一步失败
4. 根据错误信息修复

### 问题2: 找不到 Artifacts

- 确保构建成功（绿色 ✓）
- Artifacts 保留 30 天后自动删除
- 可以重新运行 workflow

### 问题3: 文件太小

如果下载的 exe 只有 50-80MB：
- 说明没有包含浏览器
- 检查 workflow 日志中的浏览器路径
- 确认使用的是 `build_with_browser.py`

## 配置文件位置

```
ota-account/.github/workflows/build-windows.yml
```

## 修改配置

### 修改触发条件

```yaml
on:
  push:
    branches: [ main, master, dev ]  # 添加更多分支
```

### 修改 Python 版本

```yaml
- name: Set up Python
  uses: actions/setup-python@v5
  with:
    python-version: "3.12"  # 改为 3.12
```

### 修改保留时间

```yaml
- name: Upload EXE artifact
  uses: actions/upload-artifact@v4
  with:
    retention-days: 90  # 改为 90 天
```

## 成本

GitHub Actions 对公开仓库**完全免费**，私有仓库每月有免费额度：
- Free: 2000 分钟/月
- Pro: 3000 分钟/月
- Team: 10000 分钟/月

每次构建约 5 分钟，所以：
- 公开仓库: 无限次
- 私有仓库 Free: 约 400 次/月

## 最佳实践

1. **使用 tag 发布正式版本**：
```bash
git tag v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

2. **开发时使用手动触发**：
   - 避免每次 push 都触发
   - 节省构建时间

3. **定期清理旧的 Artifacts**：
   - 在 Actions 页面手动删除
   - 或设置较短的保留时间

## 总结

现在你可以：
1. ✅ 在 Mac 上开发
2. ✅ 推送到 GitHub
3. ✅ 自动在 Windows 环境打包
4. ✅ 下载包含浏览器的完整 exe
5. ✅ 分发给客户使用

完全不需要本地 Windows 环境！
