# 景点推荐接口

推荐目的地的热门旅游景点。

## 接口信息

- **路径**: `/api/attraction`
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
  "message": "{\"spotList\":[{\"name\":\"武侯祠\",\"latitude\":\"30.64\",\"longitude\":\"104.05\",\"address\":\"成都市武侯区武侯祠大街231号\",\"score\":\"4.5分\",\"intro\":\"三国文化圣地\"}]}",
  "code": "200"
}
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| name | 景点名称 |
| latitude | 纬度 |
| longitude | 经度 |
| address | 地址 |
| score | 评分 |
| intro | 简介 |
