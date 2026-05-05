# Trip Planner - Backend Server

智能旅行计划后端服务，基于 LLM Agent 架构和 Flask 框架构建。

## ✨ 核心功能

### AI 智能规划
- 🤖 **多 Agent 协作** - 天气、景点、酒店、餐饮专业 Agent 协同工作
- 📋 **行程自动生成** - 输入目的地和天数，自动生成完整旅行计划
- 🎯 **偏好匹配** - 根据用户偏好标签精准推荐

### API 接口
| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/plan` | POST | 生成完整旅行计划 |
| `/api/weather` | POST | 查询目的地天气 |
| `/api/attraction` | POST | 推荐旅游景点 |
| `/api/hotel` | POST | 推荐酒店住宿 |
| `/api/restaurant` | POST | 推荐特色餐饮 |
| `/api/hotel/detail` | POST | 获取酒店详情 |
| `/api/attraction/detail` | POST | 获取景点详情 |
| `/api/restaurant/detail` | POST | 获取餐厅详情 |
| `/api/auth/register` | POST | 用户注册 |
| `/api/auth/login` | POST | 用户登录 |
| `/api/trip/save` | POST | 保存行程到云端 |
| `/api/trip/list` | GET | 获取用户行程列表 |
| `/api/trip/detail` | GET | 获取行程详情 |

## 🏗️ 技术架构

### Agent 架构
```
CoordinatorAgent (协调器)
    ├── WeatherAgent (天气查询) → 高德地图 MCP
    ├── AttractionAgent (景点推荐) → 高德地图 MCP
    ├── HotelAgent (酒店推荐) → 高德地图 MCP
    └── RestaurantAgent (餐饮推荐) → 高德地图 MCP
```

### 技术栈
- **Web 框架**: Flask + Flask-CORS
- **LLM**: 通义千问 (Qwen) via SiliconFlow
- **工具调用**: MCP (Model Context Protocol)
- **地图服务**: 高德地图 API
- **用户认证**: JWT Token
- **数据库**: SQLite (用户数据)

## 📦 项目结构

| 目录 | 说明 |
|------|------|
| `agent/base/` | Agent 基类 |
| `agent/specific/` | 各专业 Agent 实现 |
| `agent/CoordinatorAgent.py` | 多 Agent 协调器 |
| `service/` | 核心服务 (LLM、认证、MCP) |
| `tools/` | MCP 工具封装 |
| `util/` | 工具类 (日志、JSON 提取) |
| `test/` | 测试脚本 |

## 🚀 快速开始

### 1. 环境要求
- Python 3.8+
- Node.js (用于 MCP Server)

### 2. 安装依赖
```bash
pip install flask flask-cors python-dotenv
pip install mcp openai
```

### 3. 配置环境变量
复制并修改 `env/.env` 文件：
```env
# 大语言模型配置
LLM_MODEL_ID=Qwen/Qwen3-14B
LLM_API_KEY=your_api_key
LLM_BASE_URL=https://api.siliconflow.cn/v1/
LLM_TIMEOUT=300

# 高德地图配置
GAODE_KEY=your_amap_api_key
```

### 4. 启动服务
```bash
cd trip_planer
python main_api.py
```

服务默认运行在 `http://localhost:5000`

## 📡 API 使用示例

### 生成旅行计划
```bash
curl -X POST http://localhost:5000/api/plan \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "成都",
    "days": "3",
    "preferences": "经济型酒店,川菜,自然风光"
  }'
```

### 查询天气
```bash
curl -X POST http://localhost:5000/api/weather \
  -H "Content-Type: application/json" \
  -d '{
    "destination": "成都",
    "days": "3"
  }'
```

## 🔧 配置说明

### LLM 模型
支持任何 OpenAI 兼容的 API：
- SiliconFlow (默认)
- 阿里云 DashScope
- 本地部署模型

### 高德地图 MCP
需要安装高德地图 MCP Server：
```bash
npm install -g @amap/amap-maps-mcp-server
```

## 📄 License

MIT License
