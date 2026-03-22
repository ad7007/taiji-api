# 分布式记忆存储架构设计 v0.1

## 核心问题

**如何让多个服务器的记忆文件保持同步，且不互相覆盖？**

---

## 当前问题

```
传统方式：
广州服务器 MEMORY.md ←── 覆盖 ──→ 硅谷服务器 MEMORY.md
                           ↓
                    一方记忆丢失
```

**问题**：
- 直接复制会覆盖
- 无法知道哪个版本更新
- 无法追溯变更历史
- 冲突无法解决

---

## 设计目标

| 目标 | 说明 |
|------|------|
| **不丢失** | 任何服务器的记忆都不会被覆盖删除 |
| **可追溯** | 知道每条记忆的来源和时间 |
| **自动同步** | 定期自动同步，无需人工干预 |
| **冲突解决** | 明确规则处理冲突 |
| **离线容错** | 单台服务器离线不影响整体 |

---

## 方案一：Git式版本控制

```
广州服务器                        硅谷服务器
    │                                │
    ├─ MEMORY.md                     ├─ MEMORY.md
    ├─ memory/*.md                   ├─ memory/*.md
    └─ .git/                         └─ .git/
         │                                │
         └──────── .git/remote ───────────┘
                    ↓
              云端仓库（Gitee/GitHub）
```

**优点**：
- 成熟的版本控制
- 自动合并冲突
- 完整历史记录

**缺点**：
- 需要手动commit/push
- 合并冲突时需要人工决策
- 对于AI不友好

---

## 方案二：CRDT数据结构

```
MEMORY.md 不是普通文本，而是 CRDT 结构：

## 更新日志
- 2026-03-21 v1.2.0发布！ @server:gz #hash:a1b2c3
- 2026-03-22 双服务器部署 @server:sv #hash:d4e5f6
```

**CRDT（Conflict-free Replicated Data Types）**：
- 无冲突复制数据类型
- 任何服务器可以独立写入
- 自动合并，不需要协调
- 最终一致性保证

**优点**：
- 自动合并，无需人工
- 数学保证无冲突
- 适合分布式系统

**缺点**：
- 实现复杂
- 需要改造现有文件格式
- 工具支持少

---

## 方案三：时间戳+来源标记（推荐）

```
## 更新日志

### [2026-03-22 08:30:00] @gz
- 心跳协议v2完成
- 任务队列优化

### [2026-03-22 08:35:00] @sv  
- YouTube采集能力部署
- 国际API配置

### [2026-03-22 08:40:00] @gz
- 分布式同步协议设计
```

**规则**：
1. 每条记录带 `[时间戳] @来源`
2. 合并时按时间戳排序
3. 相同时间戳的冲突，按服务器优先级（gz > sv）或人工确认
4. 不删除，只追加

**优点**：
- 简单直观
- 无需改造文件格式
- AI易于理解和维护
- 可追溯

**缺点**：
- 需要可靠的时钟同步
- 人工确认时需要通知机制

---

## 推荐方案：时间戳+来源标记+版本链

### 文件格式

```markdown
# MEMORY.md - 米珞的长时记忆

---
version: v3
chain: 
  - v1 @gz 2026-03-21T10:00:00 #hash:abc123
  - v2 @sv 2026-03-22T08:00:00 #hash:def456
  - v3 @gz 2026-03-22T08:30:00 #hash:ghi789
---

## 更新日志

### 2026-03-22 @gz
- 分布式同步协议设计完成

### 2026-03-22 @sv
- YouTube采集能力部署

### 2026-03-21 @gz
- v1.2.0发布！
```

### 合并算法

```python
def merge_memory(local_path, remote_path, output_path):
    """
    合并两个MEMORY.md文件
    """
    local = parse_memory(local_path)
    remote = parse_memory(remote_path)
    
    # 1. 检查版本链
    if not has_common_ancestor(local.chain, remote.chain):
        # 没有共同祖先，需要人工确认
        return NEED_MANUAL_MERGE
    
    # 2. 提取所有记录
    all_records = []
    all_records.extend(local.records)
    all_records.extend(remote.records)
    
    # 3. 去重（相同hash的记录）
    seen = set()
    unique_records = []
    for record in all_records:
        if record.hash not in seen:
            seen.add(record.hash)
            unique_records.append(record)
    
    # 4. 按时间戳排序
    unique_records.sort(key=lambda r: r.timestamp)
    
    # 5. 写入合并结果
    write_memory(output_path, unique_records, 
                 version=local.version + 1,
                 merged_from=[local.version, remote.version])
    
    return SUCCESS
```

### 同步流程

```
同步触发（每30分钟）
    ↓
1. 本地快照（带时间戳和hash）
    ↓
2. 推送到云端（不覆盖，追加）
    ↓
3. 拉取其他服务器的快照
    ↓
4. 检测版本链是否有分歧
    ↓
    ├─ 无分歧 → 自动合并
    └─ 有分歧 → 标记冲突，通知主控
    ↓
5. 推送合并结果
    ↓
6. 更新本地版本号
```

---

## 存储结构

### 云端存储

```
gdrive:taiji-memory/
├── chain/
│   ├── v1.json          # 版本链记录
│   ├── v2.json
│   └── v3.json
├── snapshots/
│   ├── gz/
│   │   ├── 20260322_080000/
│   │   │   ├── MEMORY.md
│   │   │   ├── memory/
│   │   │   └── meta.json
│   │   └── LATEST       # 指向最新快照
│   └── sv/
│       ├── 20260322_083000/
│       └── LATEST
└── merged/
    └── MEMORY.md        # 合并后的最新版本
```

### 版本链记录

```json
// v3.json
{
  "version": 3,
  "hash": "sha256:ghi789...",
  "timestamp": "2026-03-22T08:30:00Z",
  "server": "gz",
  "parent": "v2",
  "changes": [
    "分布式同步协议设计完成"
  ],
  "merged_from": null
}
```

### 快照元数据

```json
// meta.json
{
  "server": "gz",
  "timestamp": "2026-03-22T08:30:00Z",
  "version": "v3",
  "files": {
    "MEMORY.md": "sha256:abc123...",
    "memory/2026-03-22.md": "sha256:def456..."
  },
  "agent_status": {
    "palaces": 9,
    "load": 0.7,
    "memory_usage": "25%"
  }
}
```

---

## 冲突解决

### 场景1：相同章节不同内容

```
gz: ## 用户偏好\n- 喜欢简洁\n
sv: ## 用户偏好\n- 喜欢详细\n
```

**解决**：保留两条，标记来源
```
## 用户偏好

<!-- @gz 2026-03-22T08:00:00 -->
- 喜欢简洁

<!-- @sv 2026-03-22T08:05:00 -->
- 喜欢详细

<!-- ⚠️ 冲突需确认 -->
```

### 场景2：相同记录不同服务器

```
gz: - 2026-03-22 心跳优化
sv: - 2026-03-22 心跳优化（扩展版）
```

**解决**：保留内容更多的版本，或合并

### 场景3：离线服务器重新上线

```
sv 离线3天后上线，有本地修改
```

**解决**：
1. 检测到sv版本链落后
2. 拉取云端最新版本
3. 将sv本地修改作为新版本追加
4. 不覆盖云端已有内容

---

## 实现计划

### Phase 1：基础框架
- [ ] 设计文件格式规范
- [ ] 实现快照创建脚本
- [ ] 实现基础合并脚本

### Phase 2：云端同步
- [ ] 配置rclone
- [ ] 实现push/pull命令
- [ ] 实现版本链管理

### Phase 3：自动化
- [ ] 定时同步（cron）
- [ ] 冲突检测与通知
- [ ] Web控制台查看版本历史

### Phase 4：多服务器
- [ ] 硅谷服务器部署
- [ ] 双向同步测试
- [ ] 监控告警

---

## 下一步

1. **确认方案** - 余总确认时间戳+来源标记方案是否可行
2. **改造MEMORY.md** - 按新格式添加版本链头部
3. **实现合并脚本** - 编写自动合并逻辑
4. **部署硅谷节点** - 在新服务器上部署并测试同步

---

**创建时间**: 2026-03-22
**状态**: 草案，待确认