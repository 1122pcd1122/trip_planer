# 智能旅行规划助手

基于多智能体架构的旅行规划服务，自动整合天气、景点、酒店、餐饮信息，生成完整旅行行程。

## 功能特性

- **天气查询**：获取目的地实时天气及未来多天预报
- **景点推荐**：根据城市和偏好推荐热门景点
- **酒店推荐**：智能推荐适合的住宿选择
- **餐饮推荐**：发现当地特色美食
- **行程规划**：自动生成按天划分的详细旅行计划

## 技术架构

- **后端**：FastAPI + Python
- **大语言模型**：OpenAI API (支持多模型切换)
- **地图服务**：高德地图 MCP 工具
- **架构**：多智能体协同 (Coordinator + 4 专项 Agent)

## 项目结构

```
myAgent/
├── trip_planer/
│   ├── agent/                  # 智能体模块
│   │   ├── base/               # 基础智能体
│   │   ├── specific/           # 专项智能体
│   │   │   ├── WeatherAgent.py      # 天气查询
│   │   │   ├── AttractionAgent.py  # 景点推荐
│   │   │   ├── HotelAgent.py       # 酒店推荐
│   │   │   └── RestaurantAgent.py  # 餐饮推荐
│   │   └── CoordinatorAgent.py  # 行程协调
│   ├── service/                # 服务层
│   ├── tools/                  # 工具封装
│   ├── test/                   # 测试用例
│   ├── util/                   # 工具函数
│   └── main_api.py             # API 入口
└── .env                        # 环境配置
```

## 环境配置

在 `.env` 文件中配置：

```env
# OpenAI API 配置
OPENAI_API_KEY=your_api_key
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4o-mini

# MCP 高德地图配置
AMAP_MCP_SERVER_URL=http://localhost:8000
AMAP_MCP_API_KEY=your_amap_key
```

## 启动服务

```bash
# 安装依赖
pip install -r requirements.txt

# 启动 API 服务
python -m trip_planer.main_api
```

服务默认运行在 `http://localhost:8000`

## API 接口

### 生成旅行计划

```http
POST /api/plan
Content-Type: application/json

{
    "destination": "成都",
    "days": "2",
    "preferences": "美食"
}
```

### 天气查询

```http
POST /api/weather
Content-Type: application/json

{
    "destination": "成都",
    "days": "2",
    "preferences": ""
}
```

### 景点推荐

```http
POST /api/attraction
Content-Type: application/json

{
    "destination": "成都",
    "days": "2",
    "preferences": ""
}
```

### 酒店推荐

```http
POST /api/hotel
Content-Type: application/json

{
    "destination": "成都",
    "days": "2",
    "preferences": ""
}
```

### 餐饮推荐

```http
POST /api/restaurant
Content-Type: application/json

{
    "destination": "成都",
    "days": "2",
    "preferences": ""
}
```

## 响应格式

所有接口返回统一格式：

```json
{
    "status": "success",
    "message": "返回数据",
    "code": "200"
}
```

## 旅行计划返回格式

```json
{
    "days": [
        {
            "dayNum": 1,
            "date": "2026-04-30",
            "weather": "阴",
            "itinerary": [
                {
                    "time": "09:00",
                    "spot": "宽窄巷子",
                    "address": "成都市青羊区",
                    "latitude": "",
                    "longitude": ""
                }
            ],
            "meals": {
                "lunch": {
                    "name": "龙抄手",
                    "address": "春熙路",
                    "dish": "红油抄手"
                },
                "dinner": {
                    "name": "小龙坎火锅",
                    "address": "总府路",
                    "dish": "麻辣火锅"
                }
            },
            "tips": "建议携带雨具"
        }
    ],
    "hotel": [
        {
            "name": "成都香格里拉大酒店",
            "address": "成都市锦江区滨江东路9号",
            "price": "600-1200元/晚",
            "advantage": "位于市中心春熙路商圈，交通便利",
            "latitude": "",
            "longitude": ""
        }
    ],
    "overallTips": "整体行程建议..."
}
```

## 依赖

- fastapi
- uvicorn
- openai
- pydantic
- python-dotenv

## License

MIT
