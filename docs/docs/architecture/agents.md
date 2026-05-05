# Agent 架构

本文档说明智能旅行助手的 Agent 架构设计。

## 架构概览

系统采用多 Agent 协同架构，每个 Agent 负责特定领域的任务。

```
┌─────────────────────────────────────────┐
│          CoordinatorAgent               │
│        (旅行计划协调器)                   │
└────────────┬────────────────────────────┘
             │
    ┌────────┼────────┬────────┐
    │        │        │        │
    ▼        ▼        ▼        ▼
┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐
│Weather│ │Attrac│ │Hotel │ │Restau│
│ Agent │ │tion  │ │ Agent│ │rant  │
│       │ │Agent │ │      │ │Agent │
└──────┘ └──────┘ └──────┘ └──────┘
```

## Agent 类型

### 1. CoordinatorAgent（协调器）

- **职责**: 整合其他 Agent 的结果，生成完整旅行计划
- **位置**: `agent/CoordinatorAgent.py`
- **输入**: 目的地、天数、偏好
- **输出**: 完整旅行计划 JSON

### 2. WeatherAgent（天气 Agent）

- **职责**: 查询目的地天气信息
- **位置**: `agent/specific/WeatherAgent.py`
- **工具**: 高德地图天气 API
- **输出**: 天气数据 JSON

### 3. AttractionAgent（景点 Agent）

- **职责**: 推荐热门旅游景点
- **位置**: `agent/specific/AttractionAgent.py`
- **工具**: 高德地图 POI 搜索
- **输出**: 景点列表 JSON

### 4. HotelAgent（酒店 Agent）

- **职责**: 推荐优质酒店
- **位置**: `agent/specific/HotelAgent.py`
- **工具**: 高德地图酒店搜索
- **输出**: 酒店列表 JSON

### 5. RestaurantAgent（餐厅 Agent）

- **职责**: 推荐特色美食餐厅
- **位置**: `agent/specific/RestaurantAgent.py`
- **工具**: 高德地图餐厅搜索
- **输出**: 餐厅列表 JSON

### 6. 详情 Agent

| Agent | 位置 | 职责 |
|-------|------|------|
| HotelDetailAgent | `agent/specific/HotelDetailAgent.py` | 获取酒店详情 |
| AttractionDetailAgent | `agent/specific/AttractionDetailAgent.py` | 获取景点详情 |
| RestaurantDetailAgent | `agent/specific/RestaurantDetailAgent.py` | 获取餐厅详情 |

## Agent 基类

所有 Agent 继承自 `BaseAgent`：

```python
class BaseAgent:
    def __init__(self, name: str, role_description: str):
        self.name = name
        self.system_prompt = f"你是{name}。{role_description}"
        self.messages = [{"role": "system", "content": self.system_prompt}]
        self.equipped_tools = {}
        self.tools_schema = []
    
    def run(self, user_input: str) -> str:
        # 核心运行逻辑
        pass
    
    def equip_tool(self, tool):
        # 装配工具
        pass
```

## Agent 工作流程

1. **接收任务**: 用户输入查询请求
2. **工具评估**: LLM 评估是否需要使用工具
3. **工具调用**: 执行工具获取外部数据
4. **结果总结**: LLM 根据工具结果生成回答
5. **返回结果**: 输出 JSON 格式数据
