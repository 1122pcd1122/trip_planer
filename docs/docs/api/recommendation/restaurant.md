# 餐饮推荐接口

推荐目的地的特色美食餐厅。

## 接口信息

- **路径**: `/api/restaurant`
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
  "message": "{\"restaurantList\":[{\"name\":\"小龙坎火锅\",\"latitude\":\"30.65\",\"longitude\":\"104.07\",\"address\":\"成都市锦江区\",\"score\":\"4.6分\",\"intro\":\"正宗川味火锅\"}]}",
  "code": "200"
}
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| name | 餐厅名称 |
| latitude | 纬度 |
| longitude | 经度 |
| address | 地址 |
| score | 评分 |
| intro | 简介 |
