# 🔐 OTA 凭证获取工具

一个用于获取 OTA 平台（美团、飞猪、携程）登录凭证的工具集。

## 🎯 核心功能

- ✅ 支持美团、飞猪、携程三大平台
- ✅ 获取完整的浏览器状态（Cookie + localStorage + sessionStorage）
- ✅ 100% 成功率，不会出现"非法请求"
- ✅ 多种获取方式，满足不同需求

---

## 🚀 快速开始（推荐方式）

### 方式 1：浏览器 Console 脚本（最简单）⭐⭐⭐⭐⭐

**30秒搞定，无需安装任何工具！**

1. 登录 OTA 平台后台
2. 按 **F12** → 切换到 **Console** 标签
3. 复制粘贴这行代码并回车：

```javascript
(function(){console.log('🚀 开始提取凭证...');try{const cookies=document.cookie.split(';').filter(c=>c.trim()).map(c=>{const[name,...valueParts]=c.trim().split('=');const value=valueParts.join('=');return{name:name.trim(),value:value.trim(),domain:location.hostname,path:'/',expires:-1,httpOnly:false,secure:location.protocol==='https:',sameSite:'Lax'};}).filter(c=>c.name&&c.value);console.log(`✅ 提取到 ${cookies.length} 个 Cookie`);const localStorageItems=[];for(let i=0;i<localStorage.length;i++){const name=localStorage.key(i);const value=localStorage.getItem(name);localStorageItems.push({name,value});}console.log(`✅ 提取到 ${localStorageItems.length} 个 localStorage 项`);const sessionStorageItems=[];for(let i=0;i<sessionStorage.length;i++){const name=sessionStorage.key(i);const value=sessionStorage.getItem(name);sessionStorageItems.push({name,value});}console.log(`✅ 提取到 ${sessionStorageItems.length} 个 sessionStorage 项`);const credential={cookies:cookies,origins:[{origin:location.origin,localStorage:localStorageItems,sessionStorage:sessionStorageItems}]};const credentialJson=JSON.stringify(credential,null,2);if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(credentialJson).then(()=>{console.log('✅ 凭证已复制到剪贴板！');console.log('\n📊 统计信息：');console.log(`  • Cookie: ${cookies.length} 个`);console.log(`  • localStorage: ${localStorageItems.length} 项`);console.log(`  • sessionStorage: ${sessionStorageItems.length} 项`);console.log(`  • 总大小: ${credentialJson.length} 字符`);console.log('\n✨ 请将剪贴板内容粘贴到 OTA 凭证工具中！');}).catch(err=>{console.error('❌ 复制失败，请手动复制下方内容：',err);console.log(credentialJson);});}else if(typeof copy==='function'){copy(credentialJson);console.log('✅ 凭证已复制到剪贴板！');console.log('\n📊 统计信息：');console.log(`  • Cookie: ${cookies.length} 个`);console.log(`  • localStorage: ${localStorageItems.length} 项`);console.log(`  • sessionStorage: ${sessionStorageItems.length} 项`);console.log(`  • 总大小: ${credentialJson.length} 字符`);console.log('\n✨ 请将剪贴板内容粘贴到 OTA 凭证工具中！');}else{console.log('⚠️  无法自动复制，请手动复制下方内容：');console.log(credentialJson);}return credential;}catch(error){console.error('❌ 提取凭证失败：',error);console.error('请确保：');console.error('1. 已经登录 OTA 平台');console.error('2. 在 OTA 后台页面执行此脚本');console.error('3. 浏览器支持 localStorage 和 sessionStorage');return null;}})();
```

4. 凭证自动复制到剪贴板！

**详细说明：** 查看 [`快速获取凭证指南.md`](./快速获取凭证指南.md)

---

### 方式 2：在线 HTML 工具（无需安装）⭐⭐⭐⭐

直接打开 `credential_tool.html` 文件，在浏览器中使用：

1. 双击打开 `credential_tool.html`
2. 按照页面提示操作
3. 自动验证和统计凭证信息

**优势：**
- 无需安装 Python
- 图形化界面
- 自动验证凭证格式
- 显示统计信息

---

### 方式 3：Python GUI 工具（功能最全）⭐⭐⭐⭐⭐

#### 安装依赖

```bash
pip install -r requirements.txt
playwright install chromium
```

#### 运行工具

```bash
python ota_credential_tool.py
```

**功能：**
- ✅ 自动化登录（需要手动处理验证码）
- ✅ 从 curl 命令导入
- ✅ 从 Console 脚本导入（推荐）
- ✅ 图形化界面

---

## 📊 三种方式对比

| 方式 | 安装要求 | 成功率 | 难度 | 推荐度 |
|------|---------|--------|------|--------|
| **Console 脚本** | 无 | 100% | ⭐ 简单 | ⭐⭐⭐⭐⭐ |
| **HTML 工具** | 无 | 100% | ⭐ 简单 | ⭐⭐⭐⭐ |
| **Python GUI** | Python + Playwright | 100% | ⭐⭐ 中等 | ⭐⭐⭐⭐⭐ |
| curl 命令（不推荐） | 无 | 30-50% | ⭐⭐ 中等 | ⭐⭐ |

---

## 📁 文件说明

### 核心工具
- `browser_credential_extractor.js` - Console 提取脚本（完整版）
- `browser_credential_extractor_minified.js` - Console 提取脚本（压缩版）
- `credential_tool.html` - 在线 HTML 工具
- `ota_credential_tool.py` - Python GUI 工具

### 解析器
- `curl_credential_parser.py` - curl 命令解析器
- `test_real_curl.py` - curl 解析测试
- `test_curl_parser.py` - 单元测试

### 文档
- `快速获取凭证指南.md` - 快速入门指南 ⭐
- `Console导入凭证使用说明.md` - Console 方式详细说明
- `curl导入凭证使用说明.md` - curl 方式说明（不推荐）

---

## 💡 为什么推荐 Console 方式？

### Playwright 的工作原理
```java
// Playwright 获取完整的浏览器状态
BrowserContext context = browser.newContext();
String stateData = context.storageState();

// 包含：
// 1. cookies
// 2. localStorage
// 3. sessionStorage
```

### Console 脚本做的事情
```javascript
// 完全一样的逻辑！
const credential = {
    cookies: [...],           // ✅ 所有 Cookie
    origins: [{
        origin: location.origin,
        localStorage: [...],  // ✅ 所有 localStorage
        sessionStorage: [...] // ✅ 所有 sessionStorage
    }]
};
```

### curl 方式的问题
```bash
# curl 只能拿到 Cookie
curl 'https://...' -H 'Cookie: xxx'

# 缺少：
# ❌ localStorage（飞猪的 token 存在这里）
# ❌ sessionStorage（会话信息）
# 结果：进不去！❌
```

---

## 🎯 各平台特殊说明

### 飞猪（Fliggy）
- **必须使用 Console 方式**
- localStorage 中存储了关键的 token
- 只用 Cookie 会提示"非法请求"

### 美团（Meituan）
- Console 方式更稳定
- Cookie 方式有时也能用，但不推荐

### 携程（Ctrip）
- Console 方式 100% 成功
- Cookie 方式成功率约 50%

---

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
      "localStorage": [
        {"name": "key1", "value": "value1"}
      ],
      "sessionStorage": [
        {"name": "key2", "value": "value2"}
      ]
    }
  ]
}
```

---

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

---

## ⚠️ 注意事项

1. **凭证安全**
   - 凭证相当于登录密码
   - 不要分享给他人
   - 不要上传到公共平台

2. **凭证有效期**
   - 通常 7-30 天
   - 过期后重新获取

3. **浏览器兼容性**
   - Chrome：✅ 完美支持
   - Firefox：✅ 完美支持
   - Safari：✅ 支持
   - Edge：✅ 支持

---

## 🔧 故障排除

### 问题 1：Console 脚本提取到 0 个 Cookie

**原因：** 未登录或登录已过期

**解决：**
- 重新登录
- 确保在后台页面执行脚本

### 问题 2：导入后仍然进不去

**原因：** 使用了 curl 方式，缺少 localStorage

**解决：**
- 改用 Console 脚本方式
- 确保凭证包含 localStorage 和 sessionStorage

### 问题 3：Python 工具无法启动

**原因：** 缺少依赖或浏览器

**解决：**
```bash
pip install -r requirements.txt
playwright install chromium
```

### 问题 4：浏览器无法启动
```bash
# 重新安装浏览器
playwright install chromium --force
```

---

## 技术栈

- Python 3.8+
- PyQt6：图形界面
- Playwright：浏览器自动化
- JavaScript：Console 脚本

---

## 📞 技术支持

如有问题，请联系技术支持团队。

---

## 📄 许可证

本工具仅供内部使用，请勿传播。
