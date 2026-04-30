# -*- coding: utf-8 -*-
"""
智能旅行助手 API 主入口文件

提供 RESTful API 接口，支持旅行计划生成、天气查询、景点推荐、酒店预订、餐饮推荐等功能。
所有接口均基于 FastAPI 框架实现，采用异步处理模式。

主要功能：
    - /api/plan: 生成完整旅行计划
    - /api/weather: 查询目的地天气
    - /api/attraction: 推荐旅游景点
    - /api/hotel: 推荐酒店住宿
    - /api/restaurant: 推荐特色餐饮

请求/响应格式：统一使用 JSON 格式
    - 请求体: TripPlanRequest (destination, days, preferences)
    - 响应体: TripResponse (status, message, code)
"""

import time
import json
import re
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from trip_planer.agent.CoordinatorAgent import CoordinatorAgent
from trip_planer.agent.specific.WeatherAgent import WeatherAgent
from trip_planer.agent.specific.AttractionAgent import AttractionAgent
from trip_planer.agent.specific.HotelAgent import HotelAgent
from trip_planer.agent.specific.RestaurantAgent import RestaurantAgent
from trip_planer.util.extractJson import extract_json
from trip_planer.util.logger import logger


# ==================== FastAPI 应用初始化 ====================

# 初始化 FastAPI 实例，配置 API 文档标题和描述
app = FastAPI(
    title="智能旅行助手 API",
    description="提供智能体驱动的旅行规划接口，支持旅行计划生成、天气查询、景点酒店餐饮推荐等功能"
)


# ==================== CORS 中间件配置 ====================

# 配置跨域资源共享 (CORS)，允许所有来源的请求访问 API
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # 允许所有域名访问
    allow_credentials=True,        # 允许携带认证信息
    allow_methods=["*"],           # 允许所有 HTTP 方法
    allow_headers=["*"],          # 允许所有请求头
)


# ==================== 全局 Agent 初始化 ====================

# 启动时初始化所有 Agent 实例
# Agent 是智能旅行助手的核心组件，每个 Agent 负责特定领域的任务处理
logger.info("🚀 正在启动服务器，初始化全局中枢 Agent...")

# 旅行计划协调 Agent，负责整合其他 Agent 的结果生成完整旅行计划
planner_agent = CoordinatorAgent()

# 天气查询 Agent，负责获取目的地的天气信息
weather_agent = WeatherAgent()

# 景点推荐 Agent，负责推荐旅游目的地的主要景点
attraction_agent = AttractionAgent()

# 酒店推荐 Agent，负责推荐目的地的优质酒店
hotel_agent = HotelAgent()

# 餐饮推荐 Agent，负责推荐目的地的特色美食餐厅
restaurant_agent = RestaurantAgent()


# ==================== 数据模型定义 ====================

class TripPlanRequest(BaseModel):
    """
    旅行计划请求数据模型
    
    用于接收客户端提交的旅行计划请求参数。
    
    属性说明：
        destination: 目的地城市或景点名称，如"成都"、"杭州"等
        days: 计划游玩天数，字符串格式便于 Android 端传输
        preferences: 用户偏好设置，可选字段，如"想吃火锅"、"想要海景房"等
    """
    destination: str      # 目的地
    days: str            # 游玩天数
    preferences: str = "" # 用户偏好


class TripResponse(BaseModel):
    """
    统一响应数据模型
    
    所有 API 接口均返回此格式的响应数据。
    
    属性说明：
        status: 响应状态，"success"表示成功，"error"表示失败
        message: 响应消息内容，成功时为 JSON 字符串，失败时为错误信息
        code: HTTP 状态码，200表示成功，500表示服务器内部错误
    """
    status: str          # 响应状态
    message: str         # 响应消息
    code: str = "200"   # HTTP 状态码


# ==================== 工具函数 ====================



# ==================== API 路由定义 ====================

@app.post("/api/plan")
async def generate_trip_plan(request: TripPlanRequest) -> TripResponse:
    """
    生成完整旅行计划接口
    
    调用 CoordinatorAgent 协调其他四个专项 Agent（天气、景点、酒店、餐饮），
    整合各 Agent 的返回结果，生成完整的旅行计划。
    
    请求参数：
        destination: 目的地城市
        days: 游玩天数
        preferences: 用户偏好
    
    返回值：
        TripResponse: 包含完整旅行计划的 JSON 字符串
    """
    try:
        # 调用协调 Agent 生成旅行计划
        result = planner_agent.generate_plan(
            destination=request.destination,
            days=int(request.days),        # 转换为整数
            preferences=request.preferences
        )
        logger.info(f"[DEBUG] Weather Agent原始返回: {result}")
        return TripResponse(status="success", message=result, code="200")
    except Exception as e:
        # 捕获异常并返回错误信息
        logger.error(f"生成旅行计划失败: {str(e)}")
        return TripResponse(status="error", message=str(e), code="500")


@app.get("/")
def read_root() -> TripResponse:
    """
    根路径健康检查接口
    
    用于验证 API 服务是否正常运行。
    
    返回值：
        TripResponse: 欢迎消息
    """
    return TripResponse(status="ok", message="Welcome to Smart Travel Assistant API!", code="200")


@app.post("/api/weather")
async def get_weather(request: TripPlanRequest) -> TripResponse:
    """
    天气查询接口
    
    调用天气 Agent 获取目的地的实时天气信息。
    
    请求参数：
        destination: 目的地城市
        days: 游玩天数
        preferences: 用户偏好
    
    返回值：
        TripResponse: 包含天气信息的 JSON 字符串
    """
    try:
        query_parts = [f"查询 {request.destination} 的天气情况"]
        if request.days:
            query_parts.append(f"游玩{request.days}天")
        if request.preferences:
            query_parts.append(f"偏好：{request.preferences}")
        query = "，".join(query_parts) + "。"
        result = weather_agent.run(query)
        result = extract_json(result)
        logger.info(f"[DEBUG] Weather Agent原始返回: {result}")
        return TripResponse(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"查询天气失败: {str(e)}")
        return TripResponse(status="error", message=str(e), code="500")


@app.post("/api/attraction")
async def get_attraction(request: TripPlanRequest) -> TripResponse:
    """
    景点推荐接口
    
    调用景点 Agent 推荐目的地的主要旅游景点。
    
    请求参数：
        destination: 目的地城市
        days: 游玩天数
        preferences: 用户偏好
    
    返回值：
        TripResponse: 包含景点列表的 JSON 字符串
    """
    try:
        query_parts = [f"推荐 {request.destination} 的景点"]
        if request.days:
            query_parts.append(f"游玩{request.days}天")
        if request.preferences:
            query_parts.append(f"偏好：{request.preferences}")
        query_parts.append("请推荐合适的景点数量")
        query = "，".join(query_parts) + "。"
        result = attraction_agent.run(query)
        result = extract_json(result)
        logger.info(f"[DEBUG] Attraction Agent原始返回: {result}")
        return TripResponse(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"推荐景点失败: {str(e)}")
        return TripResponse(status="error", message=str(e), code="500")


@app.post("/api/hotel")
async def get_hotel(request: TripPlanRequest) -> TripResponse:
    """
    酒店推荐接口
    
    调用酒店 Agent 推荐目的地的优质酒店。
    
    请求参数：
        destination: 目的地城市
        days: 游玩天数
        preferences: 用户偏好
    
    返回值：
        TripResponse: 包含酒店列表的 JSON 字符串
    """
    try:
        query_parts = [f"推荐 {request.destination} 的酒店"]
        if request.days:
            query_parts.append(f"游玩{request.days}天")
        if request.preferences:
            query_parts.append(f"偏好：{request.preferences}")
        query_parts.append("请推荐合适的酒店数量")
        query = "，".join(query_parts) + "。"
        result = hotel_agent.run(query)
        result = extract_json(result)
        logger.info(f"[DEBUG] Hotel Agent原始返回: {result}")
        return TripResponse(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"推荐酒店失败: {str(e)}")
        return TripResponse(status="error", message=str(e), code="500")


@app.post("/api/restaurant")
async def get_restaurant(request: TripPlanRequest) -> TripResponse:
    """
    餐饮推荐接口
    
    调用餐饮 Agent 推荐目的地的特色美食餐厅。
    
    请求参数：
        destination: 目的地城市
        days: 游玩天数
        preferences: 用户偏好
    
    返回值：
        TripResponse: 包含餐厅列表的 JSON 字符串
    """
    try:
        query_parts = [f"推荐 {request.destination} 的特色餐饮"]
        if request.days:
            query_parts.append(f"游玩{request.days}天")
        if request.preferences:
            query_parts.append(f"偏好：{request.preferences}")
        query_parts.append("请推荐合适的餐厅数量")
        query = "，".join(query_parts) + "。"
        result = restaurant_agent.run(query)
        result = extract_json(result)
        logger.info(f"[DEBUG] Restaurant Agent原始返回: {result}")
        return TripResponse(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"推荐餐饮失败: {str(e)}")
        return TripResponse(status="error", message=str(e), code="500")


# ==================== 应用入口 ====================

if __name__ == "__main__":
    """
    主程序入口
    
    启动 FastAPI 开发服务器，监听 0.0.0.0:8000
    可通过 http://localhost:8000 访问 API
    文档地址: http://localhost:8000/docs
    """
    uvicorn.run(app, host="0.0.0.0", port=8000)
