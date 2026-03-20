# Scene 使用指南

## 什么是 Scene

Scene 是任务场景的定义，用于自动组队。

## 定义 Scene

```yaml
scenes:
  scene:download:
    palace: 1
    description: 文件下载
    flow: [1, 7, 5]
```

## Scene 流程

`flow` 定义执行顺序：
- 1宫：数据采集
- 7宫：TDD验收
- 5宫：交付余总

## 触发 Scene

```python
# 通过关键词自动匹配
dispatch(scene="scene:download", payload={...})
```
