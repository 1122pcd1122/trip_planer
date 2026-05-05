# 智能旅行助手 API 文档

欢迎使用智能旅行助手 API！本系统基于 Flask 框架和 AI Agent 技术，提供智能化的旅行规划服务。

## 📖 简介

智能旅行助手是一个基于大语言模型和多 Agent 架构的旅行规划系统。通过协调多个专业 Agent（天气、景点、酒店、餐饮），为用户提供完整的旅行计划。

## ✨ 核心特性

- 🌤️ **天气查询** - 获取目的地实时天气信息
- 🏞️ **景点推荐** - 智能推荐热门旅游景点
- 🏨 **酒店推荐** - 推荐优质住宿选择
- 🍽️ **餐饮推荐** - 发现当地特色美食
- 📋 **完整计划** - 生成多日旅行行程规划
- 🔍 **详情查询** - 获取酒店、景点、餐厅详细信息

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install flask flask-cors
```

### 2. 启动服务

```bash
cd Agent
python -m trip_planer.main_api
```

### 3. 测试接口

```bash
python -m trip_planer.test.test_api
```

## 📡 API 概览

| 接口类型 | 路径 | 方法 | 说明 |
|---------|------|------|------|
| 健康检查 | `/` | GET | 验证服务状态 |
| 旅行计划 | `/api/plan` | POST | 生成完整旅行计划 |
| 天气查询 | `/api/weather` | POST | 查询目的地天气 |
| 景点推荐 | `/api/attraction` | POST | 推荐旅游景点 |
| 酒店推荐 | `/api/hotel` | POST | 推荐酒店住宿 |
| 餐饮推荐 | `/api/restaurant` | POST | 推荐特色餐饮 |
| 酒店详情 | `/api/hotel/detail` | POST | 获取酒店详细信息 |
| 景点详情 | `/api/attraction/detail` | POST | 获取景点详细信息 |
| 餐厅详情 | `/api/restaurant/detail` | POST | 获取餐厅详细信息 |

## 📦 统一响应格式

所有接口返回统一的 JSON 格式：

```json
{
  "status": "success",
  "message": "响应内容（JSON字符串）",
  "code": "200"
}
```

## 🏗️ 架构设计

系统采用多 Agent 协同架构：

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

## 📚 文档导航

- [快速开始](getting-started/installation.md) - 安装和配置指南
- [API 接口](api/overview.md) - 详细接口文档
- [数据模型](models/request.md) - 请求和响应格式
- [架构设计](architecture/agents.md) - 系统架构说明

## 🛠️ 技术栈

- **后端框架**: Flask
- **AI 模型**: 大语言模型 (LLM)
- **地图服务**: 高德地图 API
- **文档工具**: MkDocs Material

## 📝 许可证

Copyright © 2024 Trip Planner Team
