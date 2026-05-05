# 天气查询接口

查询目的地的天气信息，为旅行计划提供参考。

## 接口信息

- **路径**: `/api/weather`
- **方法**: `POST`
- **Content-Type**: `application/json`

## 请求参数

```json
{
  "destination": "成都",
  "days": "2",
  "preferences": ""
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| destination | string | ✅ | 目的地城市 |
| days | string | ❌ | 游玩天数 |
| preferences | string | ❌ | 用户偏好 |

## 响应示例

```json
{
  "status": "success",
  "message": "{\"weather\":{\"temperature\":\"20-25°C\",\"condition\":\"多云\",\"humidity\":\"65%\",\"wind\":\"微风\"}}",
  "code": "200"
}
```
