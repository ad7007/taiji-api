# 分布式智能体同步协议 v1.0

## 核心原则

**不删除，只合并** — 类似Git merge，而非Git push --force

---

## 智能体"灵魂"组成

| 层级 | 文件 | 同步策略 |
|------|------|----------|
| **记忆层** | MEMORY.md, memory/*.md | 合并（去重+时间戳） |
| **配置层** | openclaw.json | 最新优先 |
| **会话层** | agents/*/sessions/*.jsonl | 追加，不覆盖 |
| **技能层** | skills/ | 双向同步 |
| **数据库层** | memory/*.sqlite | SQLite合并 |

---

## 同步流程

```
同步触发（定时/手动）
    ↓
1. 本地快照（带时间戳）
    ↓
2. 拉取云端状态
    ↓
3. 三向合并（本地 + 云端 + 基线）
    ↓
4. 冲突检测与解决
    ↓
5. 推送合并结果
    ↓
6. 更新基线版本号
```

---

## 实现脚本

### 1. 创建智能体快照

```bash
#!/bin/bash
# snapshot-agent.sh

TIMESTAMP=$(date +%Y%m%d_%H%M%S)
SNAPSHOT_DIR="/tmp/agent-snapshot-$TIMESTAMP"

mkdir -p "$SNAPSHOT_DIR"

# 1. 记忆层
cp ~/.openclaw/workspace/MEMORY.md "$SNAPSHOT_DIR/"
cp -r ~/.openclaw/workspace/memory "$SNAPSHOT_DIR/"

# 2. 配置层
cp ~/.openclaw/openclaw.json "$SNAPSHOT_DIR/"

# 3. 会话层（增量）
find ~/.openclaw/agents -name "*.jsonl" -newer ~/.openclaw/.last-sync -exec cp {} "$SNAPSHOT_DIR/sessions/" \;

# 4. 技能层清单
ls ~/.openclaw/workspace/skills > "$SNAPSHOT_DIR/skills-manifest.txt"

# 5. 数据库
cp ~/.openclaw/memory/*.sqlite "$SNAPSHOT_DIR/db/"

# 创建元数据
echo "{\"timestamp\": \"$TIMESTAMP\", \"server\": \"$HOSTNAME\"}" > "$SNAPSHOT_DIR/meta.json"

echo "快照已创建: $SNAPSHOT_DIR"
```

### 2. 合并记忆文件

```python
#!/usr/bin/env python3
# merge_memory.py

import os
import re
from datetime import datetime

def merge_memory_files(local_path, remote_path, output_path):
    """合并两个MEMORY.md文件，保留时间戳较新的内容"""
    
    def parse_sections(content):
        """解析MEMORY.md的章节结构"""
        sections = {}
        current_section = None
        current_content = []
        
        for line in content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = [line]
            else:
                current_content.append(line)
        
        if current_section:
            sections[current_section] = '\n'.join(current_content)
        
        return sections
    
    with open(local_path, 'r') as f:
        local_sections = parse_sections(f.read())
    
    with open(remote_path, 'r') as f:
        remote_sections = parse_sections(f.read())
    
    # 合并策略：以local为基础，补充remote的新内容
    merged = local_sections.copy()
    
    for section_name, content in remote_sections.items():
        if section_name not in merged:
            merged[section_name] = content
        else:
            # 检查时间戳
            local_time = extract_latest_timestamp(merged[section_name])
            remote_time = extract_latest_timestamp(content)
            
            if remote_time and (not local_time or remote_time > local_time):
                merged[section_name] = content
    
    # 写入合并结果
    with open(output_path, 'w') as f:
        for section_name in sorted(merged.keys()):
            f.write(merged[section_name] + '\n')
    
    return merged

def extract_latest_timestamp(content):
    """提取内容中最新时间戳"""
    timestamps = re.findall(r'(\d{4}-\d{2}-\d{2})', content)
    if timestamps:
        return max(timestamps)
    return None

if __name__ == '__main__':
    import sys
    merge_memory_files(sys.argv[1], sys.argv[2], sys.argv[3])
```

### 3. 云端同步（基于rclone）

```bash
#!/bin/bash
# sync-to-cloud.sh

RCLONE_REMOTE="gdrive:openclaw-distributed"
LOCAL_DIR="$HOME/.openclaw"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. 上传本地快照（不覆盖云端）
rclone copy "$LOCAL_DIR" "$RCLONE_REMOTE/snapshots/$HOSTNAME/$TIMESTAMP" \
    --exclude "node_modules/**" \
    --exclude "*.log" \
    --exclude "sessions/*.jsonl.deleted.*"

# 2. 下载其他服务器的快照
rclone sync "$RCLONE_REMOTE/merged" "/tmp/merged-state" --dry-run

# 3. 执行合并
python3 /root/.openclaw/workspace/skills/taiji-nine-palaces/scripts/merge_memory.py \
    "$LOCAL_DIR/workspace/MEMORY.md" \
    "/tmp/merged-state/MEMORY.md" \
    "$LOCAL_DIR/workspace/MEMORY.md"

# 4. 上传合并结果
rclone copy "$LOCAL_DIR/workspace/MEMORY.md" "$RCLONE_REMOTE/merged/"

echo "同步完成: $TIMESTAMP"
```

---

## 冲突解决规则

| 冲突类型 | 解决策略 |
|----------|----------|
| 同一章节不同内容 | 时间戳优先 |
| 同一天memory文件 | 按服务器ID分节合并 |
| 配置冲突 | 人工确认 |
| sessions.jsonl冲突 | 全部保留（追加） |

---

## 区块链式版本链

```
genesis (初始部署)
    ↓
v1_20260321_gz (广州服务器快照)
    ↓
v2_20260321_la (洛杉矶服务器快照)
    ↓
v3_20260322_merged (合并版本)
    ↓
...
```

每个版本包含：
- 哈希值（SHA256）
- 父版本哈希
- 时间戳
- 服务器来源
- 变更摘要

---

## 快速部署

```bash
# 1. 安装rclone（如未安装）
curl https://rclone.org/install.sh | sudo bash

# 2. 配置远程存储
rclone config

# 3. 初始化分布式状态
bash /root/.openclaw/workspace/skills/taiji-nine-palaces/scripts/init-distributed.sh

# 4. 设置定时同步（每30分钟）
(crontab -l 2>/dev/null; echo "*/30 * * * * /root/.openclaw/workspace/skills/taiji-nine-palaces/scripts/sync-to-cloud.sh") | crontab -
```

---

## 恢复流程

```bash
# 从任意服务器恢复完整状态
rclone sync "gdrive:openclaw-distributed/merged" ~/.openclaw/workspace/

# 恢复配置
rclone sync "gdrive:openclaw-distributed/config" ~/.openclaw/

# 重启服务
openclaw restart
```

---

## 监控与告警

- 同步失败 → 飞书通知
- 冲突检测 → 人工确认
- 版本链断裂 → 自动修复

---

**维护宫位**: 5宫米珞 + 6宫监控
**创建时间**: 2026-03-22