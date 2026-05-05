# 健康检查接口

验证 API 服务是否正常运行。

## 接口信息

- **路径**: `/`
- **方法**: `GET`
- **认证**: 无需认证

## 请求示例

```bash
curl http://localhost:8000/
```

## 响应示例

### 成功响应

```json
{
  "status": "ok",
  "message": "Welcome to Smart Travel Assistant API!",
  "code": "200"
}
```

## 状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 服务正常运行 |

## 用途

- 服务健康检查
- 负载均衡器健康探测
- 部署验证
