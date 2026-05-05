# 景点详情接口

获取特定景点的详细信息。

## 接口信息

- **路径**: `/api/attraction/detail`
- **方法**: `POST`
- **Content-Type**: `application/json`

## 请求参数

```json
{
  "name": "武侯祠",
  "type": "attraction",
  "latitude": "30.64",
  "longitude": "104.05"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | string | ✅ | 景点名称 |
| type | string | ✅ | 类型（固定为 "attraction"） |
| latitude | string | ❌ | 纬度 |
| longitude | string | ❌ | 经度 |

## 响应示例

```json
{
  "status": "success",
  "message": "{\"name\":\"武侯祠\",\"address\":\"成都市武侯区武侯祠大街231号\",\"phone\":\"028-85555555\",\"rating\":\"4.5分\",\"ticketPrice\":\"50元\",\"openTime\":\"08:00-18:00\",\"suggestion\":\"建议游览2-3小时\",\"history\":\"三国文化圣地\",\"description\":\"中国唯一的君臣合祀祠庙\",\"bestTime\":\"春季和秋季\",\"duration\":\"2-3小时\"}",
  "code": "200"
}
```

## 输出字段说明

| 字段 | 说明 |
|------|------|
| name | 景点名称 |
| address | 景点地址 |
| phone | 联系电话 |
| rating | 评分 |
| ticketPrice | 门票价格 |
| openTime | 开放时间 |
| suggestion | 游览建议 |
| history | 历史文化背景 |
| description | 景点简介 |
| bestTime | 最佳游览时间 |
| duration | 建议游览时长 |
