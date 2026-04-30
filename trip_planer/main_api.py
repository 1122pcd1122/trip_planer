import time
import json
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
from trip_planer.util.logger import logger

# 1. 初始化 FastAPI 实例
app = FastAPI(
    title="智能旅行助手 API",
    description="提供智能体驱动的旅行规划接口"
)

# 2. 配置跨域 (CORS)
# noinspection PyTypeChecker
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
logger.info("🚀 正在启动服务器，初始化全局中枢 Agent...")

# 3. 实例化全局中枢 Agent
planner_agent = CoordinatorAgent()
weather_agent = WeatherAgent()
attraction_agent = AttractionAgent()
hotel_agent = HotelAgent()
restaurant_agent = RestaurantAgent()


# 3. 数据模型定义 (确立前后端数据契约)
class TripRequest(BaseModel):
    destination: str  # 目的地，例如："成都"
    days: int  # 游玩天数，例如：3
    preferences: str = ""  # 用户偏好，默认为空，例如："想吃火锅，行程不要太赶"

class SingleAgentRequest(BaseModel):
    destination: str

class TripResponse(BaseModel):
    status: str
    message: str
    code: str = "200"


import re


def extract_json(result: str) -> str:
    """
    从【普通文本字符串】中提取JSON
    无markdown处理，仅匹配 {} 或 [] 格式的JSON
    兜底返回合法空JSON，永不报错
    """
    # 空值直接返回空对象
    if not result or not isinstance(result, str):
        return "{}"

    # 清理首尾空白
    text = result.strip()

    # 核心：匹配 完整JSON对象 { ... } 或 JSON数组 [ ... ]
    # 支持多行、换行、空格，兼容纯字符串内的JSON
    json_pattern = r'(\{.*\}|\[.*\])'
    match = re.search(json_pattern, text, re.DOTALL)

    if match:
        return match.group(0).strip()

    # 未找到JSON，返回空对象（保证json.loads一定能解析）
    return "{}"


@app.post("/api/plan/stream")
async def generate_trip_plan(request: TripRequest) -> TripResponse:
    """汇总Agent接口 - 一次性返回完整JSON"""
    try:
        result = planner_agent.generate_plan(
            destination=request.destination,
            days=request.days,
            preferences=request.preferences
        )
        return TripResponse(status="success", message=result, code="200")
    except Exception as e:
        return TripResponse(status="error", message=str(e), code="500")

@app.get("/")
def read_root() -> TripResponse:
    return TripResponse(status="ok", message="Welcome to Smart Travel Assistant API!", code="200")


@app.post("/api/weather")
async def get_weather(request: SingleAgentRequest) -> TripResponse:
    """天气查询Agent接口 - 一次性返回完整JSON"""
    try:
        result = weather_agent.run(f"请查询 {request.destination} 的天气情况。")
        return TripResponse(status="success", message=extract_json(result), code="200")
    except Exception as e:
        return TripResponse(status="error", message=str(e), code="500")


@app.post("/api/attraction")
async def get_attraction(request: SingleAgentRequest) -> TripResponse:
    """景点推荐Agent接口 - 一次性返回完整JSON"""
    try:
        result = attraction_agent.run(f"请推荐 {request.destination} 的景点。")
        return TripResponse(status="success", message=extract_json(result), code="200")
    except Exception as e:
        return TripResponse(status="error", message=str(e), code="500")


@app.post("/api/hotel")
async def get_hotel(request: SingleAgentRequest) -> TripResponse:
    """酒店推荐Agent接口 - 一次性返回完整JSON"""
    try:
        result = hotel_agent.run(f"请推荐 {request.destination} 的酒店。")
        return TripResponse(status="success", message=extract_json(result), code="200")
    except Exception as e:
        return TripResponse(status="error", message=str(e), code="500")


@app.post("/api/restaurant")
async def get_restaurant(request: SingleAgentRequest) -> TripResponse:
    """餐饮推荐Agent接口 - 一次性返回完整JSON"""
    try:
        result = restaurant_agent.run(f"请推荐 {request.destination} 的特色餐饮。")
        return TripResponse(status="success", message=extract_json(result), code="200")
    except Exception as e:
        return TripResponse(status="error", message=str(e), code="500")


if __name__ == "__main__":
    # 启动命令
    uvicorn.run(app, host="0.0.0.0", port=8000)