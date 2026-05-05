# 酒店详情接口

获取特定酒店的详细信息。

## 接口信息

- **路径**: `/api/hotel/detail`
- **方法**: `POST`
- **Content-Type**: `application/json`

## 请求参数

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
| name | string | ✅ | 酒店名称 |
| type | string | ✅ | 类型（固定为 "hotel"） |
| latitude | string | ❌ | 纬度 |
| longitude | string | ❌ | 经度 |

## 响应示例

```json
{
  "status": "success",
  "message": "{\"name\":\"成都香格里拉大酒店\",\"address\":\"成都市锦江区滨江东路9号\",\"phone\":\"028-88888888\",\"rating\":\"4.8分\",\"priceRange\":\"800-1200元\",\"feature\":\"江景房、豪华泳池\",\"facilities\":\"WiFi、停车场、游泳池、健身房\",\"roomTypes\":\"豪华大床房、行政套房\",\"checkInTime\":\"14:00\",\"checkOutTime\":\"12:00\",\"description\":\"豪华五星级酒店\"}",
  "code": "200"
}
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| name | 酒店名称 |
| address | 酒店地址 |
| phone | 联系电话 |
| rating | 评分 |
| priceRange | 价格区间 |
| feature | 酒店特色/亮点 |
| facilities | 设施列表 |
| roomTypes | 房型介绍 |
| checkInTime | 入住时间 |
| checkOutTime | 退房时间 |
| description | 酒店简介 |
