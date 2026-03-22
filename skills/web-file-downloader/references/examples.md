# 使用示例

本文档包含针对不同平台的具体使用案例。

---

## 示例1：太极平台下载工作流配置

### 场景
从太极平台下载某个工作流的拓扑配置文件。

### 配置

```bash
export TARGET_URL="https://a.taiji.woa.com/workflow/xxx"
export FILE_NAME="topology.json"
export TASK_NAME="taiji_workflow_backup"
export PAGE_ANCHOR_TEXT="配置文件"
export SIDEBAR_CONTAINER=".ant-drawer"
export FILE_MANAGER_BTN_TEXT="文件管理"
export FILE_TABLE_SELECTOR=".ant-modal table"
export DOWNLOAD_OP_INDEX=0
```

### 执行步骤

1. 打开太极平台工作流页面
2. 选中目标节点（触发参数侧边栏显示）
3. 运行下载流程

```bash
# 验证配置
source ~/.openclaw/workspace/skills/web-file-downloader/scripts/platform-configs.sh
bash ~/.openclaw/workspace/skills/web-file-downloader/scripts/validate_config.sh

# 执行下载
# （通过 OpenClaw 浏览器自动化执行 SKILL.md 中的流程）
```

### 预期结果
文件保存到：`~/Downloads/taiji_workflow_backup_20240315_143022/topology.json`

---

## 示例2：腾讯云导出服务器配置

### 场景
从腾讯云控制台导出 CVM 实例的配置信息。

### 配置

```bash
export TARGET_URL="https://console.cloud.tencent.com/cvm"
export FILE_NAME="cvm_config.json"
export TASK_NAME="tencent_cvm_backup"
export PAGE_ANCHOR_TEXT="导出配置"
export SIDEBAR_CONTAINER=".tc-dialog"
export FILE_MANAGER_BTN_TEXT="导出"
export FILE_TABLE_SELECTOR=".tc-table"
export DOWNLOAD_OP_INDEX=0
```

### 执行步骤

1. 进入腾讯云 CVM 控制台
2. 选中目标实例
3. 点击"更多操作" → "导出配置"
4. 运行下载流程

---

## 示例3：批量下载多个文件

### 场景
从同一个页面批量下载多个配置文件。

### 脚本

```bash
#!/bin/bash
# batch_download.sh

FILES=("config.json" "model.py" "requirements.txt")
TASK_BASE="project_backup"

for file in "${FILES[@]}"; do
    export FILE_NAME="$file"
    export TASK_NAME="${TASK_BASE}_${file%.*}"
    
    echo "下载: $file"
    bash ~/.openclaw/workspace/skills/web-file-downloader/scripts/process_download.sh
done

echo "批量下载完成"
```

---

## 示例4：定时自动备份

### 场景
每天自动备份重要配置。

### Cron 配置

```bash
# 添加到 crontab
0 2 * * * cd /path/to/project && bash backup_configs.sh >> /var/log/config_backup.log 2>&1
```

### backup_configs.sh

```bash
#!/bin/bash
export TARGET_URL="https://a.taiji.woa.com/workflow/important"
export FILE_NAME="critical_config.json"
export TASK_NAME="daily_backup"
export OUTPUT_DIR="/backup/configs"

# 验证并下载
bash ~/.openclaw/workspace/skills/web-file-downloader/scripts/validate_config.sh
bash ~/.openclaw/workspace/skills/web-file-downloader/scripts/process_download.sh

# 保留最近30天的备份
find /backup/configs -name "daily_backup_*" -type d -mtime +30 -exec rm -rf {} +
```

---

## 示例5：适配新平台

### 场景
公司内部有一个新的数据平台需要适配。

### 步骤

1. **分析页面结构**

```javascript
// 在浏览器控制台执行
// 找到文件管理按钮
const btn = document.querySelector('[text*="下载"], [text*="导出"]');
console.log('按钮:', btn);

// 找到文件表格
const table = document.querySelector('table');
console.log('表格:', table);

// 找到侧边栏
const sidebar = document.querySelector('.drawer, .panel, [class*="side"]');
console.log('侧边栏:', sidebar);
```

2. **提取选择器**

```bash
# 记录找到的选择器
export CUSTOM_URL="data.internal.company.com"
export CUSTOM_ANCHOR="下载中心"
export CUSTOM_SIDEBAR=".data-panel"
export CUSTOM_FILE_BTN="导出数据"
export CUSTOM_TABLE=".data-table"
export CUSTOM_OP_INDEX=0
```

3. **测试配置**

```bash
# 验证选择器是否能正确定位
curl -s "data.internal.company.com" | grep -E "(下载|导出|文件管理)"
```

4. **添加到平台配置**

编辑 `scripts/platform-configs.sh`，添加新平台配置。

---

## 常见问题

### Q: 下载按钮点击后没有反应？
A: 检查 `DOWNLOAD_OP_INDEX`，有些平台下载按钮在操作列的第1个位置（索引1）而非第0个。

### Q: 页面加载很慢，总是超时？
A: 增加等待时间：
```bash
export WAIT_SECONDS=5  # 默认是2秒
```

### Q: 下载的文件名不对？
A: 检查 `FILE_NAME` 是否设置正确，或者使用通配符匹配：
```bash
export FILE_NAME="*.json"  # 下载第一个匹配的json文件
```

### Q: 如何下载多个文件？
A: 使用批量下载脚本（见示例3），或者多次调用流程，每次更换 `FILE_NAME`。
