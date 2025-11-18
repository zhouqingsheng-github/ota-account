# OTA凭证获取工具

这是一个用于获取OTA平台（美团、飞猪、携程）登录凭证的桌面工具。

## 功能特性

- ✅ 支持美团、飞猪、携程三大OTA平台
- ✅ 图形化界面，操作简单
- ✅ 自动化登录流程
- ✅ 获取浏览器凭证（cookies + localStorage）
- ✅ 一键复制凭证

## 安装步骤

### 1. 安装Python依赖

```bash
cd ota-account
pip install -r requirements.txt
```

### 2. 安装Playwright浏览器

```bash
playwright install chromium
```

## 使用方法

### 启动工具

```bash
python ota_credential_tool.py
```

### 操作步骤

1. **选择OTA渠道**：从下拉框选择美团、飞猪或携程
2. **输入账号**：填写OTA平台的登录账号
3. **输入密码**：填写OTA平台的登录密码
4. **点击"获取凭证"**：工具会打开浏览器自动登录
5. **处理验证**：如果出现验证码或滑块，请手动完成
6. **获取凭证**：登录成功后，凭证会自动显示在文本框中
7. **复制凭证**：点击"复制凭证"按钮，将凭证复制到剪贴板

## 凭证格式

获取的凭证是JSON格式，包含：
- `cookies`: 浏览器Cookie信息
- `origins`: localStorage和sessionStorage信息

示例：
```json
{
  "cookies": [
    {
      "name": "token",
      "value": "xxx",
      "domain": ".meituan.com",
      "path": "/",
      "expires": 1234567890,
      "httpOnly": true,
      "secure": true,
      "sameSite": "Lax"
    }
  ],
  "origins": [
    {
      "origin": "https://e.dianping.com",
      "localStorage": []
    }
  ]
}
```

## 注意事项

1. **验证码处理**：部分平台可能需要手动完成验证码或滑块验证
2. **登录超时**：默认等待120秒，如果超时请重试
3. **凭证有效期**：获取的凭证有时效性，建议及时使用
4. **安全性**：请妥善保管凭证，不要泄露给他人

## 与Java后端集成

获取的凭证可以直接用于Java后端的`OtaAccountState.contextData`字段：

```java
OtaAccountState state = new OtaAccountState();
state.setAccountId(accountId);
state.setPlatformCode("meituan"); // 或 "fliggy", "ctrip"
state.setStoreId(storeId);
state.setContextData(credential); // 从工具复制的凭证
state.setLoginStatus(1);
state.setStatus(1);
accountStateService.saveOrUpdateStateByAccountId(state);
```

## 故障排查

### 问题1：浏览器无法启动
```bash
# 重新安装浏览器
playwright install chromium --force
```

### 问题2：登录失败
- 检查账号密码是否正确
- 检查网络连接
- 尝试手动完成验证码

### 问题3：凭证无效
- 凭证可能已过期，重新获取
- 检查平台是否正确

## 技术栈

- Python 3.8+
- PyQt6：图形界面
- Playwright：浏览器自动化

## 开发者

如需修改或扩展功能，请参考：
- `ota_credential_tool.py`：主程序文件
- `LoginWorker`类：登录逻辑
- `OTACredentialTool`类：UI界面
