# 酒店推荐接口

推荐目的地的优质酒店住宿。

## 接口信息

- **路径**: `/api/hotel`
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
  "message": "{\"hotelList\":[{\"name\":\"成都香格里拉大酒店\",\"latitude\":\"30.65\",\"longitude\":\"104.07\",\"address\":\"成都市锦江区滨江东路9号\",\"priceRange\":\"800-1200元\",\"feature\":\"江景房、豪华泳池\"}]}",
  "code": "200"
}
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| name | 酒店名称 |
| latitude | 纬度 |
| longitude | 经度 |
| address | 地址 |
| priceRange | 价格区间 |
| feature | 特色/亮点 |
