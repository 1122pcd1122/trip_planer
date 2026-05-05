# 服务流程

本文档说明智能旅行助手的完整服务流程。

## 请求处理流程

```
客户端请求
    │
    ▼
Flask 路由接收
    │
    ▼
参数验证
    │
    ▼
调用对应 Agent
    │
    ▼
Agent 执行任务
    │
    ├── 调用 LLM 评估
    │
    ├── 执行工具（如需）
    │
    └── 生成结果
    │
    ▼
提取 JSON
    │
    ▼
封装响应
    │
    ▼
返回客户端
```

## 旅行计划生成流程

```
POST /api/plan
    │
    ▼
CoordinatorAgent.generate_plan()
    │
    ├── WeatherAgent.run() ────── 天气数据
    │
    ├── AttractionAgent.run() ─── 景点列表
    │
    ├── HotelAgent.run() ──────── 酒店列表
    │
    └── RestaurantAgent.run() ─── 餐厅列表
    │
    ▼
整合所有数据
    │
    ▼
生成完整旅行计划
    │
    ▼
返回 JSON 响应
```

## 详情查询流程

```
POST /api/hotel/detail
    │
    ▼
HotelDetailAgent.run()
    │
    ├── 接收酒店名称和坐标
    │
    ├── 调用高德地图工具
    │
    └── 获取详细信息
    │
    ▼
提取 JSON
    │
    ▼
返回响应
```

## 错误处理

```
try:
    # 执行任务
    result = agent.run(query)
    result = extract_json(result)
    return make_response("success", result, "200")
except Exception as e:
    logger.error(f"错误: {str(e)}")
    return make_response("error", str(e), "500")
```

## 日志记录

系统使用统一的日志记录：

```python
from trip_planer.util.logger import logger

logger.info("信息")
logger.error("错误")
logger.warning("警告")
```
