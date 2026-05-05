# 旅行计划接口

生成完整的旅行计划，协调多个 Agent 生成包含天气、景点、酒店、餐饮的综合行程。

## 接口信息

- **路径**: `/api/plan`
- **方法**: `POST`
- **Content-Type**: `application/json`

## 请求参数

```json
{
  "destination": "成都",
  "days": "2",
  "preferences": "和女朋友"
}
```

| 字段 | 类型 | 必填 | 说明 | 示例 |
|------|------|------|------|------|
| destination | string | ✅ | 目的地城市 | "成都" |
| days | string | ✅ | 游玩天数 | "2" |
| preferences | string | ❌ | 用户偏好 | "和女朋友" |

## 响应示例

### 成功响应

```json
{
  "status": "success",
  "message": "{\"days\":[{\"day\":1,\"weather\":{...},\"attractions\":[...],\"hotel\":{...},\"restaurants\":[...]},{\"day\":2,...}],\"overallTips\":\"出行建议\"}",
  "code": "200"
}
```

### 错误响应

```json
{
  "status": "error",
  "message": "目的地不能为空",
  "code": "400"
}
```

## 请求示例

### cURL

```bash
curl -X POST http://localhost:8000/api/plan \
  -H "Content-Type: application/json" \
  -d '{"destination":"成都","days":"2","preferences":"和女朋友"}'
```

### Python

```python
import requests

response = requests.post("http://localhost:8000/api/plan", json={
    "destination": "成都",
    "days": "2",
    "preferences": "和女朋友"
})
print(response.json())
```

## 注意事项

- 响应时间较长，需要等待 LLM 生成
- 建议设置合理的超时时间
- message 字段包含 JSON 字符串，需要二次解析
