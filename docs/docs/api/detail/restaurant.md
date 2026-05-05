# 餐厅详情接口

获取特定餐厅的详细信息。

## 接口信息

- **路径**: `/api/restaurant/detail`
- **方法**: `POST`
- **Content-Type**: `application/json`

## 请求参数

```json
{
  "name": "小龙坎火锅",
  "type": "restaurant",
  "latitude": "30.65",
  "longitude": "104.07"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 餐厅名称 |
| type | string | ✅ | 类型（固定为 "restaurant"） |
| latitude | string | ❌ | 纬度 |
| longitude | string | ❌ | 经度 |

## 响应示例

```json
{
  "status": "success",
  "message": "{\"name\":\"小龙坎火锅\",\"address\":\"成都市锦江区\",\"phone\":\"028-66666666\",\"rating\":\"4.6分\",\"avgPrice\":\"100元/人\",\"openTime\":\"10:00-22:00\",\"featureDish\":\"毛肚、鸭肠、黄喉\",\"description\":\"正宗川味火锅\",\"cuisineType\":\"川菜/火锅\",\"seats\":\"200个座位\"}",
  "code": "200"
}
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| name | 餐厅名称 |
| address | 餐厅地址 |
| phone | 联系电话 |
| rating | 评分 |
| avgPrice | 人均消费 |
| openTime | 营业时间 |
| featureDish | 招牌菜/特色菜 |
| description | 餐厅简介 |
| cuisineType | 菜系类型 |
| seats | 座位数/环境描述 |
