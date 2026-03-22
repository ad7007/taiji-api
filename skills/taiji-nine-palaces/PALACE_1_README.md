# 1-数据采集宫 - 太极平台文件下载集成

## 概述

**1-数据采集宫** 负责从太极平台工作流页面自动下载配置文件、模型文件等。

### 职责
- ✅ 从太极平台自动下载文件
- ✅ 批量下载配置文件
- ✅ 规范落盘和目录管理
- ✅ 实时更新宫位负载状态

---

## 快速开始

### 1. 基础下载

```python
from skills.taiji-nine-palaces.palace_1_data_collection import Palace1DataCollection

# 创建采集器
collector = Palace1DataCollection()

# 下载单个文件
result = collector.download_file(
    topo_name="我的拓扑",
    file_name="config.json"
)

if result["success"]:
    print(f"下载成功：{result['path']}")
```

### 2. 批量下载

```python
# 批量下载多个文件
files = ["config.json", "model.py", "data.csv"]
result = collector.batch_download(
    files=files,
    topo_name="测试拓扑"
)

print(f"成功：{result['success_count']}/{result['total']}")
```

### 3. 命令行工具

```bash
# 使用 web-file-downloader 技能
bash /root/.openclaw/workspace/skills/web-file-downloader/scripts/setup_wizard.sh

# 配置太极平台
export TARGET_URL="https://a.taiji.woa.com/..."
export FILE_NAME="config.json"
bash /root/.openclaw/workspace/skills/web-file-downloader/scripts/process_download.sh
```

---

## 配置参数

### 环境变量

```bash
# 必需参数
export TARGET_URL="https://a.taiji.woa.com/workflow/xxx"  # 目标页面
export FILE_NAME="config.json"                            # 文件名
export OUTPUT_DIR="~/Downloads/taiji-files"               # 输出目录

# 可选参数
export TASK_NAME="my_topo"                                # 任务名称
export TAIJI_DOMAIN="a.taiji.woa.com"                     # 太极域名
```

### 平台配置（太极平台）

```bash
# 太极平台特定配置
PAGE_ANCHOR_TEXT="配置文件"
SIDEBAR_CONTAINER=".ant-drawer"
FILE_MANAGER_BTN_TEXT="文件管理"
FILE_TABLE_SELECTOR=".ant-modal table"
DOWNLOAD_OP_INDEX=0
```

---

## 工作流程

```
1. 页面预检
   ├─ 验证 URL
   ├─ 等待页面加载
   └─ 确认关键文本

2. 定位文件管理
   ├─ 语义定位（文本锚点）
   ├─ 结构定位（UI 容器）
   └─ 样式定位（兜底方案）

3. 执行下载
   ├─ 打开文件管理弹窗
   ├─ 定位目标文件
   └─ 点击下载按钮

4. 文件落盘
   ├─ 等待下载完成
   ├─ 处理临时文件
   └─ 规范命名保存

5. 更新状态
   └─ 更新 1-数据采集宫负载
```

---

## 与九宫格集成

### 负载状态

| 负载值 | 含义 | 触发场景 |
|--------|------|----------|
| 0.0 | 空闲 | 无下载任务 |
| 0.3 | 任务开始 | 开始下载 |
| 0.6 | 任务完成 | 下载成功 |
| 0.2 | 任务失败 | 下载失败 |

### 阴阳平衡

**1-数据采集** 与 **2-产品质量** 形成阴阳对：

- **1-数据采集** (数据) - 收集执行数据
- **2-产品质量** (需求) - 需求与质量把控

平衡度 < 0.7 时会触发告警，需要调整两个宫位的负载。

---

## 目录结构

```
~/Downloads/taiji-files/
├── 测试拓扑_20260317_162553/
│   ├── config.json
│   └── model.py
├── 生产拓扑_20260317_170000/
│   └── config.json
└── ...
```

---

## 失败恢复

### 问题 1：找不到文件管理按钮

**解决**：
1. 确认已选中正确的节点
2. 滚动侧边栏确保按钮可见
3. 检查是否有权限限制

### 问题 2：下载后无临时文件

**解决**：
1. 等待 2-3 秒后重试
2. 确认 Chrome 下载路径为 `~/Downloads`
3. 检查是否有其他下载任务干扰

### 问题 3：页面定位失败

**解决**：
1. 使用 `detect_platform.sh` 检测平台类型
2. 调整 `PAGE_ANCHOR_TEXT` 配置
3. 尝试备选定位策略

---

## 配套脚本

| 脚本 | 功能 |
|------|------|
| `detect_platform.sh` | 自动检测页面平台类型 |
| `process_download.sh` | 处理临时下载文件 |
| `validate_config.sh` | 验证配置参数 |
| `error_recovery.sh` | 错误恢复和重试 |
| `setup_wizard.sh` | 交互式配置向导 |

---

## API 集成

### 更新宫位负载

```bash
curl -X POST http://localhost:8000/api/taiji/update-palace-load \
  -H "Content-Type: application/json" \
  -d '{"palace_id": 1, "load": 0.6}'
```

### 查看当前状态

```bash
curl http://localhost:8000/api/taiji/palace/1
```

### 批量更新（下载多个文件后）

```bash
curl -X POST http://localhost:8000/api/taiji/batch-update-palaces \
  -H "Content-Type: application/json" \
  -d '{
    "palaces": [
      {"palace_id": 1, "load": 0.6},
      {"palace_id": 2, "load": 0.7}
    ]
  }'
```

---

## 使用示例

### 示例 1：下载配置文件

```python
from skills.taiji-nine-palaces.palace_1_data_collection import Palace1DataCollection

collector = Palace1DataCollection()

# 下载配置文件
result = collector.download_file(
    topo_name="用户增长模型",
    file_name="config.json"
)

if result["success"]:
    print(f"✅ 下载成功：{result['path']}")
else:
    print(f"❌ 下载失败：{result['error']}")
```

### 示例 2：批量下载并监控

```python
files = ["config.json", "model.py", "params.yaml"]
result = collector.batch_download(files, "生产环境")

# 显示统计
print(f"总计：{result['total']}")
print(f"成功：{result['success_count']}")
print(f"失败：{result['total'] - result['success_count']}")

# 检查平衡状态
from skills.taiji-nine-palaces.taiji_client import TaijiClient
client = TaijiClient()
balance = client.get_balance_status()
print(f"阴阳平衡：{balance}")
```

---

## 注意事项

1. **浏览器要求**：需要 Chrome 浏览器和 OpenClaw 浏览器自动化工具
2. **权限要求**：需要有太极平台的访问权限
3. **下载目录**：默认为 `~/Downloads/taiji-files`
4. **临时文件**：依赖 Chrome 的 `.com.google.Chrome.*` 命名模式
5. **时区设置**：时间戳使用 Asia/Shanghai 时区

---

## 相关文件

- **技能定义**: `/root/.openclaw/workspace/skills/taiji-nine-palaces/SKILL.md`
- **Python 客户端**: `/root/.openclaw/workspace/skills/taiji-nine-palaces/palace_1_data_collection.py`
- **通用下载器**: `/root/.openclaw/workspace/skills/web-file-downloader/SKILL.md`
- **配置脚本**: `/root/.openclaw/workspace/skills/web-file-downloader/scripts/`
