# API 接口概览

智能旅行助手提供 9 个 RESTful API 接口，涵盖旅行规划的各个方面。

## 接口列表

### 基础接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 健康检查 | GET | `/` | 验证服务状态 |
| 旅行计划 | POST | `/api/plan` | 生成完整旅行计划 |
| 天气查询 | POST | `/api/weather` | 查询目的地天气 |

### 推荐接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 景点推荐 | POST | `/api/attraction` | 推荐旅游景点 |
| 酒店推荐 | POST | `/api/hotel` | 推荐酒店住宿 |
| 餐饮推荐 | POST | `/api/restaurant` | 推荐特色餐饮 |

### 详情接口

| 接口 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 酒店详情 | POST | `/api/hotel/detail` | 获取酒店详细信息 |
| 景点详情 | POST | `/api/attraction/detail` | 获取景点详细信息 |
| 餐厅详情 | POST | `/api/restaurant/detail` | 获取餐厅详细信息 |

## 统一请求格式

### 推荐类接口请求格式

```json
{
  "destination": "成都",
  "days": "2",
  "preferences": "和女朋友"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| destination | string | ✅ | 目的地城市 |
| days | string | ✅ | 游玩天数 |
| preferences | string | ❌ | 用户偏好 |

### 详情类接口请求格式

```json
{
  "name": "成都香格里拉大酒店",
  "type": "hotel",
  "latitude": "30.65",
  "longitude": "104.07"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 名称（酒店/景点/餐厅） |
| type | string | ✅ | 类型：hotel/attraction/restaurant |
| latitude | string | ❌ | 纬度 |
| longitude | string | ❌ | 经度 |

## 统一响应格式

所有接口返回统一的 JSON 格式：

```json
{
  "status": "success",
  "message": "响应内容（JSON字符串）",
  "code": "200"
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| status | string | 响应状态：success/error |
| message | string | 响应内容，成功时为 JSON 字符串，失败时为错误信息 |
| code | string | HTTP 状态码：200/500 |

## 错误码说明

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 500 | 服务器内部错误 |

## 使用示例

### cURL 示例

```bash
# 健康检查
curl http://localhost:8000/

# 生成旅行计划
curl -X POST http://localhost:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination":"成都","days":"2","preferences":"和女朋友"}'

# 查询酒店详情
curl -X POST http://localhost:8000/api/hotel/detail \
  -H "Content-Type: application/json" \
  -d '{"name":"成都香格里拉大酒店","type":"hotel"}'
```

### Python 示例

```python
import requests

BASE_URL = "http://localhost:8000"

# 生成旅行计划
response = requests.post(f"{BASE_URL}/api/plan", json={
    "destination": "成都",
    "days": "2",
    "preferences": "和女朋友"
})
print(response.json())
```
