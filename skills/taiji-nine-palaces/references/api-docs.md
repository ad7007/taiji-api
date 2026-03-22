# 太极 API 文档

## 基础端点

```
Base URL: http://localhost:8000
```

## 九宫状态

```
GET /api/taiji/palaces
```

返回所有宫位状态。

## 阴阳平衡

```
GET /api/taiji/balance
```

返回系统平衡状态。

## 更新负载

```
POST /api/taiji/update-palace-load
Content-Type: application/json

{
  "palace_id": 1,
  "load": 0.8
}
```

## 切换模式

```
POST /api/taiji/switch-mode
Content-Type: application/json

{
  "mode": "yang"
}
```
