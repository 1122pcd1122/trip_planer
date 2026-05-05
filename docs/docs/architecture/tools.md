# 工具系统

本文档说明智能旅行助手的工具系统设计。

## 工具管理器

工具管理器位于 `service/McpToolManager.py`，负责管理和提供外部工具。

## 高德地图工具

### 工具功能

- 天气查询
- POI 搜索（景点、酒店、餐厅）
- 地理编码
- 路径规划

### 工具使用

```python
from trip_planer.service.McpToolManager import tool_manager

# 获取高德地图工具
amap_tool = tool_manager.get_amap_tools()

# 装配到 Agent
agent.equip_tool(amap_tool)
```

## 工具调用流程

```
┌─────────────┐
│  Agent 接收  │
│   用户输入   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ LLM 评估    │
│ 是否需要工具 │
└──────┬──────┘
       │
  ┌────┴────┐
  │         │
  ▼         ▼
需要工具   不需要工具
  │         │
  ▼         ▼
┌──────┐ ┌──────┐
│执行  │ │直接  │
│工具  │ │回答  │
└──┬───┘ └──┬───┘
   │        │
   ▼        ▼
┌──────┐ ┌──────┐
│LLM   │ │返回  │
│总结  │ │结果  │
└──┬───┘ └──────┘
   │
   ▼
┌──────┐
│返回  │
│结果  │
└──────┘
```

## 工具 Schema

工具使用 OpenAI 函数调用格式：

```json
{
  "type": "function",
  "function": {
    "name": "weather_query",
    "description": "查询天气信息",
    "parameters": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "description": "城市名称"
        }
      },
      "required": ["city"]
    }
  }
}
```
