# 运行测试

本指南介绍如何运行 API 接口测试。

## 测试脚本

项目提供了完整的测试脚本：`trip_planer/test/test_api.py`

## 运行测试

### 1. 启动服务

首先确保 API 服务已启动：

```bash
python -m trip_planer.main_api
```

### 2. 运行测试

在新终端中运行：

```bash
python -m trip_planer.test.test_api
```

### 3. 交互式测试

测试脚本提供交互式菜单：

```
🚀 开始测试 Flask API 接口...

==================================================
1. 测试健康检查接口 (GET /)
==================================================
状态码: 200
返回结果: {
  "status": "ok",
  "message": "Welcome to Smart Travel Assistant API!",
  "code": "200"
}

请选择要测试的接口（输入数字，多个用逗号分隔，如 1,2,3）：
1. 旅行计划生成
2. 天气查询
3. 景点推荐
4. 酒店推荐
5. 餐饮推荐
6. 酒店详情
7. 景点详情
8. 餐厅详情
9. 全部测试
0. 退出

请输入选择:
```

## 测试选项

| 选项 | 说明 | 接口 |
|------|------|------|
| 1 | 旅行计划生成 | POST /api/plan |
| 2 | 天气查询 | POST /api/weather |
| 3 | 景点推荐 | POST /api/attraction |
| 4 | 酒店推荐 | POST /api/hotel |
| 5 | 餐饮推荐 | POST /api/restaurant |
| 6 | 酒店详情 | POST /api/hotel/detail |
| 7 | 景点详情 | POST /api/attraction/detail |
| 8 | 餐厅详情 | POST /api/restaurant/detail |
| 9 | 全部测试 | 所有接口 |

## 测试示例

### 测试单个接口

```
请输入选择: 2
```

### 测试多个接口

```
请输入选择: 1,2,3
```

### 测试全部接口

```
请输入选择: 9
```

## 自定义测试

可以修改 `test_api.py` 中的测试参数：

```python
# 修改测试数据
payload = {
    "destination": "成都",  # 修改目的地
    "days": "2",            # 修改天数
    "preferences": "和女朋友"  # 修改偏好
}
```

## 注意事项

- 测试需要 LLM API 响应，可能耗时较长
- 确保网络连接正常
- 确保 API 密钥配置正确
