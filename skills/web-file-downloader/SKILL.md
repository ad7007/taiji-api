---
name: web-file-downloader
description: 通用的浏览器自动化文件下载技能。在任意网页平台自动定位文件管理区域、下载文件并规范落盘。适用于内部管理平台、云控制台、数据系统等有文件下载功能的网页。触发词包括"下载网页文件"、"自动下载"、"批量下载配置文件"等。
---

# web-file-downloader

通用的浏览器自动化文件下载技能，支持在各类网页平台（太极、云控制台、数据系统等）自动下载文件。

## 核心能力

- **页面预检** - 确认目标URL和页面加载状态
- **智能定位** - 分层定位文件管理区域（语义→结构→样式）
- **自动下载** - 点击下载并监控浏览器临时文件
- **规范落盘** - 自动重命名并保存到结构化目录

## 使用方法

### 1. 配置参数

在使用前需要配置以下参数（可通过环境变量或调用时传入）：

```bash
# 必需参数
TARGET_URL="https://a.taiji.woa.com/..."          # 目标页面URL
FILE_NAME="config.json"                           # 要下载的文件名
OUTPUT_DIR="~/Downloads"                          # 下载基目录

# 定位参数（根据目标平台调整）
PAGE_ANCHOR_TEXT="配置文件"                        # 页面文本锚点
SIDEBAR_CONTAINER=".ant-drawer"                   # 侧边栏容器选择器
FILE_MANAGER_BTN_TEXT="文件管理"                   # 文件管理按钮文本
FILE_TABLE_SELECTOR=".ant-modal table"            # 文件表格选择器
DOWNLOAD_OP_INDEX=0                               # 下载按钮在操作列中的索引
```

### 2. 执行流程

#### 步骤1：页面预检

```javascript
// 确认URL和页面状态
const currentUrl = window.location.href;
if (!currentUrl.includes(TARGET_URL_PATTERN)) {
  throw new Error(`不在目标页面，当前: ${currentUrl}`);
}

// 等待关键元素出现
await waitForElement(`text=${PAGE_ANCHOR_TEXT}`);
```

#### 步骤2：定位文件管理区域

**优先级1：语义定位（推荐）**
- 通过可见文本找锚点：`配置文件`、`参数配置`、`文件管理`
- 从锚点向上找最近的表单区块/抽屉容器

**优先级2：结构定位**
- 查找常见UI框架容器：`.ant-drawer`、`.ant-form`、参数区块
- 在容器内验证是否存在"文件输入框 + 操作按钮"组合

**优先级3：样式定位（兜底）**
- 用class模糊匹配：`*[class*="drawer"]`, `*[class*="config"]`
- 必须结合文本二次校验

#### 步骤3：打开文件列表

```javascript
// 点击文件管理入口
const fileManagerBtn = await locateByText(FILE_MANAGER_BTN_TEXT);
await fileManagerBtn.click();

// 等待弹窗出现
await waitForElement(FILE_TABLE_SELECTOR);
```

#### 步骤4：定位并下载目标文件

```javascript
// 在表格中查找目标文件行
const rows = document.querySelectorAll(`${FILE_TABLE_SELECTOR} tr`);
const targetRow = [...rows].find(r => r.textContent.includes(FILE_NAME));

if (!targetRow) throw new Error(`未找到文件: ${FILE_NAME}`);

// 点击下载按钮
const ops = targetRow.querySelectorAll('a,button');
if (!ops.length) throw new Error('未找到下载操作按钮');
ops[DOWNLOAD_OP_INDEX].click();
```

#### 步骤5：处理下载文件并落盘

```bash
#!/bin/bash
# 配置
base_dir="${OUTPUT_DIR:-~/Downloads}"
task_name="${TASK_NAME:-download}"
file_name="${FILE_NAME:-downloaded_file}"

# 清洗任务名，避免路径非法字符
safe_name=$(echo "$task_name" | tr '/:' '_' | tr -s ' ' '_' | sed 's/[^[:alnum:]_.-]/_/g')

# 当前时间（Asia/Shanghai）
now=$(TZ=Asia/Shanghai date +%Y%m%d_%H%M%S)
out_dir=$(eval echo "$base_dir")/${safe_name}_${now}
mkdir -p "$out_dir"

# 等待下载完成（Chrome临时文件）
sleep 2

# 取最新Chrome临时下载文件
temp_file=$(ls -t ~/Downloads/.com.google.Chrome.* 2>/dev/null | head -1)

# 安全检查
if [ -z "$temp_file" ]; then
  echo "错误：未发现临时下载文件"
  exit 1
fi

# 移动并重命名
mv "$temp_file" "$out_dir/$file_name"
echo "下载完成: $out_dir/$file_name"
```

## OpenClaw 浏览器自动化模板

### 完整执行流程

```typescript
// 1. 获取目标标签页
const tabs = await browser.tabs({ profile: "chrome" });
const targetTab = tabs.find(t => t.url?.includes(TARGET_URL_PATTERN));

if (!targetTab) {
  // 导航到目标页面
  await browser.navigate({ 
    profile: "chrome", 
    url: TARGET_URL 
  });
}

// 2. 快照并验证页面状态
const snapshot = await browser.snapshot({ 
  profile: "chrome", 
  targetId: targetTab.id,
  refs: "aria" 
});

// 确认页面已加载关键元素
if (!snapshot.text.includes(PAGE_ANCHOR_TEXT)) {
  throw new Error("页面未加载完成，缺少关键文本锚点");
}

// 3. 定位并点击文件管理按钮
const fileManagerRef = findRefByText(snapshot, FILE_MANAGER_BTN_TEXT);
await browser.act({
  profile: "chrome",
  targetId: targetTab.id,
  request: { kind: "click", ref: fileManagerRef }
});

// 4. 等待弹窗并快照
await sleep(1000);
const modalSnapshot = await browser.snapshot({
  profile: "chrome",
  targetId: targetTab.id,
  refs: "aria"
});

// 5. 在弹窗中定位目标文件行
const fileRowRef = findRefByText(modalSnapshot, FILE_NAME);
const rowSnapshot = await browser.snapshot({
  profile: "chrome",
  targetId: targetTab.id,
  ref: fileRowRef
});

// 6. 点击下载按钮
const downloadBtnRef = findDownloadButton(rowSnapshot);
await browser.act({
  profile: "chrome",
  targetId: targetTab.id,
  request: { kind: "click", ref: downloadBtnRef }
});

// 7. 执行本地落盘脚本
await exec(`bash ${__dirname}/scripts/process_download.sh`);
```

## 平台适配示例

### 太极平台（a.taiji.woa.com）

```bash
TARGET_URL="a.taiji.woa.com"
PAGE_ANCHOR_TEXT="配置文件"
SIDEBAR_CONTAINER=".ant-drawer"
FILE_MANAGER_BTN_TEXT="文件管理"
FILE_TABLE_SELECTOR=".ant-modal table"
DOWNLOAD_OP_INDEX=0
```

### 腾讯云控制台

```bash
TARGET_URL="console.cloud.tencent.com"
PAGE_ANCHOR_TEXT="下载配置"
SIDEBAR_CONTAINER=".tc-dialog"
FILE_MANAGER_BTN_TEXT="导出"
FILE_TABLE_SELECTOR=".tc-table"
DOWNLOAD_OP_INDEX=0
```

### 通用数据平台

```bash
TARGET_URL="data.example.com"
PAGE_ANCHOR_TEXT="文件列表"
SIDEBAR_CONTAINER=".file-panel"
FILE_MANAGER_BTN_TEXT="下载"
FILE_TABLE_SELECTOR=".file-table"
DOWNLOAD_OP_INDEX=0
```

## 失败恢复策略

### 问题：找不到侧边栏
- 回到步骤1重做URL与加载校验
- 确认是否已选中正确节点/区域
- 改用"文本锚点 + 向上回溯容器"重新定位

### 问题：找不到文件管理按钮
- 确认当前区域是否有文件配置参数
- 滚动侧边栏，避免按钮在可视区外
- 检查是否有权限/只读状态导致按钮隐藏

### 问题：下载后无临时文件
- 等待1-3秒后重试
- 确认Chrome下载路径是否为默认`~/Downloads`
- 排除并发下载干扰（按时间戳过滤最新文件）

## 最佳实践

1. **始终先做页面预检** - 确认URL和加载状态后再操作
2. **分层定位** - 语义文本 → 结构容器 → 样式兜底
3. **关键步骤加断言** - 每个操作后验证预期结果
4. **下载成功判定** - 以"本地出现重命名文件"为准，不只是"点击成功"
5. **规范命名** - 使用 `{任务名}_{时间戳}` 目录格式

## 配套脚本

技能目录包含以下实用脚本：

| 脚本 | 功能 |
|------|------|
| `scripts/process_download.sh` | 处理 Chrome 临时下载文件并规范落盘 |
| `scripts/validate_config.sh` | 验证配置参数是否完整正确 |
| `scripts/detect_platform.sh` | 自动检测当前页面所属平台类型 |
| `scripts/error_recovery.sh` | 错误恢复和重试机制 |
| `scripts/setup_wizard.sh` | 交互式配置向导（推荐新手使用） |
| `scripts/platform-configs.sh` | 常见平台的预设配置模板 |

### 快速开始

```bash
# 方式1：使用配置向导（推荐）
bash ~/.openclaw/workspace/skills/web-file-downloader/scripts/setup_wizard.sh

# 方式2：手动配置
source ~/.openclaw/workspace/skills/web-file-downloader/scripts/platform-configs.sh
export TARGET_URL="..."
export FILE_NAME="..."
bash ~/.openclaw/workspace/skills/web-file-downloader/scripts/validate_config.sh
```

## 注意事项

- 此技能需要 Chrome 浏览器和 OpenClaw 浏览器自动化工具
- 下载目录默认为 `~/Downloads`，可通过 `OUTPUT_DIR` 修改
- 临时文件检测依赖 Chrome 的 `.com.google.Chrome.*` 命名模式
- 时间戳使用 Asia/Shanghai 时区
