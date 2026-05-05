# -*- coding: utf-8 -*-
"""
智能旅行助手 API 主入口文件

提供 RESTful API 接口，支持旅行计划生成、天气查询、景点推荐、酒店预订、餐饮推荐等功能。
所有接口均基于 Flask 框架实现。

主要功能：
    - /api/plan: 生成完整旅行计划
    - /api/weather: 查询目的地天气
    - /api/attraction: 推荐旅游景点
    - /api/hotel: 推荐酒店住宿
    - /api/restaurant: 推荐特色餐饮
    - /api/hotel/detail: 获取酒店详情
    - /api/attraction/detail: 获取景点详情
    - /api/restaurant/detail: 获取餐厅详情

请求/响应格式：统一使用 JSON 格式
    - 请求体: {destination, days, preferences}
    - 响应体: {status, message, code}
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json

from trip_planer.agent.CoordinatorAgent import CoordinatorAgent
from trip_planer.agent.specific.WeatherAgent import WeatherAgent
from trip_planer.agent.specific.AttractionAgent import AttractionAgent
from trip_planer.agent.specific.HotelAgent import HotelAgent
from trip_planer.agent.specific.RestaurantAgent import RestaurantAgent
from trip_planer.agent.specific.HotelDetailAgent import HotelDetailAgent
from trip_planer.agent.specific.AttractionDetailAgent import AttractionDetailAgent
from trip_planer.agent.specific.RestaurantDetailAgent import RestaurantDetailAgent
from trip_planer.service.AuthService import AuthService
from trip_planer.util.extractJson import extract_json
from trip_planer.util.logger import logger


# ==================== Flask 应用初始化 ====================

# 初始化 Flask 实例
app = Flask(__name__)

# 配置跨域资源共享 (CORS)，允许所有来源的请求访问 API
CORS(app, resources={r"/*": {"origins": "*"}})


# ==================== 全局 Agent 初始化 ====================

logger.info("🚀 正在启动服务器，初始化全局 Agent...")

planner_agent = CoordinatorAgent()
weather_agent = WeatherAgent()
attraction_agent = AttractionAgent()
hotel_agent = HotelAgent()
restaurant_agent = RestaurantAgent()
hotel_detail_agent = HotelDetailAgent()
attraction_detail_agent = AttractionDetailAgent()
restaurant_detail_agent = RestaurantDetailAgent()

auth_service = AuthService()
logger.info("🔐 用户认证服务初始化完成")


# ==================== 工具函数 ====================

def make_response(status: str, message: str, code: str = "200"):
    """
    创建统一的 JSON 响应
    
    参数：
        status: 响应状态，"success" 或 "error"
        message: 响应消息内容
        code: HTTP 状态码
    
    返回：
        Flask JSON 响应对象
    """
    return jsonify({
        "status": status,
        "message": message,
        "code": code
    })


def validate_json_output(json_str: str, expected_keys: list = None) -> str:
    """
    校验 Agent 输出的 JSON 格式
    
    参数：
        json_str: JSON 字符串
        expected_keys: 期望的顶层键列表（如 ["weatherList", "spotList"]）
    
    返回：
        校验后的 JSON 字符串，如果校验失败返回 "{}"
    """
    try:
        parsed = json.loads(json_str)
        if expected_keys:
            for key in expected_keys:
                if key not in parsed:
                    logger.warning(f"⚠️ JSON 缺少期望的键: {key}")
        return json_str
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON 格式校验失败: {str(e)}")
        logger.error(f"   原始内容: {json_str[:200]}...")
        return "{}"


# ==================== API 路由定义 ====================

@app.route("/", methods=["GET"])
def read_root():
    """
    根路径健康检查接口
    
    用于验证 API 服务是否正常运行。
    """
    return make_response(
        status="ok",
        message="Welcome to Smart Travel Assistant API!",
        code="200"
    )


@app.route("/api/plan", methods=["POST"])
def generate_trip_plan():
    """
    生成完整旅行计划接口
    
    调用 CoordinatorAgent 协调其他四个专项 Agent（天气、景点、酒店、餐饮），
    整合各 Agent 的返回结果，生成完整的旅行计划。
    
    请求参数（JSON）：
        destination: 目的地城市
        days: 游玩天数（兼容旧版）
        startDate: 开始日期（YYYY-MM-DD，新版）
        endDate: 结束日期（YYYY-MM-DD，新版）
        preferences: 用户偏好（可选）
    """
    try:
        data = request.get_json()
        destination = data.get("destination", "")
        days = data.get("days", "1")
        start_date = data.get("startDate", "")
        end_date = data.get("endDate", "")
        preferences = data.get("preferences", "")
        
        if not destination:
            return make_response(status="error", message="目的地不能为空", code="400")
        
        # 优先使用日期范围，兼容旧版天数参数
        if start_date and end_date:
            from datetime import datetime
            try:
                d1 = datetime.strptime(start_date, "%Y-%m-%d")
                d2 = datetime.strptime(end_date, "%Y-%m-%d")
                days = str((d2 - d1).days + 1)
            except ValueError:
                return make_response(status="error", message="日期格式错误，请使用 YYYY-MM-DD", code="400")
        
        # 调用协调 Agent 生成旅行计划
        result = planner_agent.generate_plan(
            destination=destination,
            days=int(days),
            preferences=preferences
        )
        result = extract_json(result)
        result = validate_json_output(result, ["days", "hotel", "overallTips"])
        logger.info(f"[DEBUG] Plan Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"生成旅行计划失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/auth/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        email = data.get("email", "")
        
        if not username or not password:
            return make_response(status="error", message="用户名和密码不能为空", code="400")
        
        return auth_service.register(username, password, email)
    except Exception as e:
        logger.error(f"注册失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/auth/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        username = data.get("username", "")
        password = data.get("password", "")
        
        if not username or not password:
            return make_response(status="error", message="用户名和密码不能为空", code="400")
        
        return auth_service.login(username, password)
    except Exception as e:
        logger.error(f"登录失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/auth/verify", methods=["POST"])
def verify_token():
    try:
        data = request.get_json()
        token = data.get("token", "")
        
        if not token:
            return make_response(status="error", message="Token 不能为空", code="400")
        
        return auth_service.verify_token(token)
    except Exception as e:
        logger.error(f"Token 验证失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/trip/save", methods=["POST"])
def save_trip():
    try:
        data = request.get_json()
        token = data.get("token", "")
        
        payload = auth_service._verify_token(token)
        if not payload:
            return make_response(status="error", message="Token 无效或已过期", code="401")
        
        return auth_service.save_trip(
            user_id=payload["user_id"],
            trip_id=data.get("trip_id", ""),
            destination=data.get("destination", ""),
            days=data.get("days", 1),
            start_date=data.get("start_date", ""),
            end_date=data.get("end_date", ""),
            preferences=data.get("preferences", ""),
            trip_data=data.get("trip_data", "")
        )
    except Exception as e:
        logger.error(f"保存行程失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/trip/list", methods=["POST"])
def get_trips():
    try:
        data = request.get_json()
        token = data.get("token", "")
        
        payload = auth_service._verify_token(token)
        if not payload:
            return make_response(status="error", message="Token 无效或已过期", code="401")
        
        return auth_service.get_trips(user_id=payload["user_id"])
    except Exception as e:
        logger.error(f"获取行程列表失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/trip/get", methods=["POST"])
def get_trip():
    try:
        data = request.get_json()
        token = data.get("token", "")
        trip_id = data.get("trip_id", "")
        
        payload = auth_service._verify_token(token)
        if not payload:
            return make_response(status="error", message="Token 无效或已过期", code="401")
        
        if not trip_id:
            return make_response(status="error", message="行程 ID 不能为空", code="400")
        
        return auth_service.get_trip(user_id=payload["user_id"], trip_id=trip_id)
    except Exception as e:
        logger.error(f"获取行程失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/trip/delete", methods=["POST"])
def delete_trip():
    try:
        data = request.get_json()
        token = data.get("token", "")
        trip_id = data.get("trip_id", "")
        
        payload = auth_service._verify_token(token)
        if not payload:
            return make_response(status="error", message="Token 无效或已过期", code="401")
        
        if not trip_id:
            return make_response(status="error", message="行程 ID 不能为空", code="400")
        
        return auth_service.delete_trip(user_id=payload["user_id"], trip_id=trip_id)
    except Exception as e:
        logger.error(f"删除行程失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/weather", methods=["POST"])
def get_weather():
    """
    天气查询接口
    
    调用天气 Agent 获取目的地的实时天气信息。
    
    请求参数（JSON）：
        destination: 目的地城市
        days: 游玩天数（兼容旧版）
        startDate: 开始日期（YYYY-MM-DD，新版）
        endDate: 结束日期（YYYY-MM-DD，新版）
        preferences: 用户偏好（可选）
    """
    try:
        data = request.get_json()
        destination = data.get("destination", "")
        days = data.get("days", "")
        start_date = data.get("startDate", "")
        end_date = data.get("endDate", "")
        preferences = data.get("preferences", "")
        
        query_parts = [f"查询 {destination} 的天气情况"]
        if start_date and end_date:
            query_parts.append(f"时间：{start_date} 至 {end_date}")
        elif days:
            query_parts.append(f"游玩{days}天")
        if preferences:
            query_parts.append(f"偏好标签：{preferences}")
        query = "，".join(query_parts) + "。"
        
        result = weather_agent.run(query)
        result = extract_json(result)
        result = validate_json_output(result, ["weatherList"])
        logger.info(f"[DEBUG] Weather Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"查询天气失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/attraction", methods=["POST"])
def get_attraction():
    """
    景点推荐接口
    
    调用景点 Agent 推荐目的地的主要旅游景点。
    
    请求参数（JSON）：
        destination: 目的地城市
        days: 游玩天数（兼容旧版）
        startDate: 开始日期（YYYY-MM-DD，新版）
        endDate: 结束日期（YYYY-MM-DD，新版）
        preferences: 用户偏好（可选）
    """
    try:
        data = request.get_json()
        destination = data.get("destination", "")
        days = data.get("days", "")
        start_date = data.get("startDate", "")
        end_date = data.get("endDate", "")
        preferences = data.get("preferences", "")
        
        query_parts = [f"推荐 {destination} 的景点"]
        if start_date and end_date:
            query_parts.append(f"时间：{start_date} 至 {end_date}")
        elif days:
            query_parts.append(f"游玩{days}天")
        if preferences:
            query_parts.append(f"偏好标签：{preferences}")
        query_parts.append("请推荐合适的景点数量")
        query = "，".join(query_parts) + "。"
        
        result = attraction_agent.run(query)
        result = extract_json(result)
        result = validate_json_output(result, ["spotList"])
        logger.info(f"[DEBUG] Attraction Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"推荐景点失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/hotel", methods=["POST"])
def get_hotel():
    """
    酒店推荐接口
    
    调用酒店 Agent 推荐目的地的优质酒店。
    
    请求参数（JSON）：
        destination: 目的地城市
        days: 游玩天数（兼容旧版）
        startDate: 开始日期（YYYY-MM-DD，新版）
        endDate: 结束日期（YYYY-MM-DD，新版）
        preferences: 用户偏好（可选）
    """
    try:
        data = request.get_json()
        destination = data.get("destination", "")
        days = data.get("days", "")
        start_date = data.get("startDate", "")
        end_date = data.get("endDate", "")
        preferences = data.get("preferences", "")
        
        query_parts = [f"推荐 {destination} 的酒店"]
        if start_date and end_date:
            query_parts.append(f"时间：{start_date} 至 {end_date}")
        elif days:
            query_parts.append(f"游玩{days}天")
        if preferences:
            query_parts.append(f"偏好标签：{preferences}")
        query_parts.append("请推荐合适的酒店数量")
        query = "，".join(query_parts) + "。"
        
        result = hotel_agent.run(query)
        result = extract_json(result)
        result = validate_json_output(result, ["hotelList"])
        logger.info(f"[DEBUG] Hotel Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"推荐酒店失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/restaurant", methods=["POST"])
def get_restaurant():
    """
    餐饮推荐接口
    
    调用餐饮 Agent 推荐目的地的特色美食餐厅。
    
    请求参数（JSON）：
        destination: 目的地城市
        days: 游玩天数（兼容旧版）
        startDate: 开始日期（YYYY-MM-DD，新版）
        endDate: 结束日期（YYYY-MM-DD，新版）
        preferences: 用户偏好（可选）
    """
    try:
        data = request.get_json()
        destination = data.get("destination", "")
        days = data.get("days", "")
        start_date = data.get("startDate", "")
        end_date = data.get("endDate", "")
        preferences = data.get("preferences", "")
        
        query_parts = [f"推荐 {destination} 的特色餐饮"]
        if start_date and end_date:
            query_parts.append(f"时间：{start_date} 至 {end_date}")
        elif days:
            query_parts.append(f"游玩{days}天")
        if preferences:
            query_parts.append(f"偏好标签：{preferences}")
        query_parts.append("请推荐合适的餐厅数量")
        query = "，".join(query_parts) + "。"
        
        result = restaurant_agent.run(query)
        result = extract_json(result)
        result = validate_json_output(result, ["foodList"])
        logger.info(f"[DEBUG] Restaurant Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"推荐餐饮失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/hotel/detail", methods=["POST"])
def get_hotel_detail():
    """
    酒店详情接口
    
    获取特定酒店的详细信息，包括设施、房型、用户评价等。
    
    请求参数（JSON）：
        name: 酒店名称
        type: 类型（固定为 "hotel"）
        latitude: 纬度（可选）
        longitude: 经度（可选）
    """
    try:
        data = request.get_json()
        name = data.get("name", "")
        latitude = data.get("latitude", "")
        longitude = data.get("longitude", "")
        
        if not name:
            return make_response(status="error", message="酒店名称不能为空", code="400")
        
        query = f"请查询酒店【{name}】的详细信息，包括设施、房型、评分、联系方式等。坐标({latitude}, {longitude})。"
        result = hotel_detail_agent.run(query)
        result = extract_json(result)
        logger.info(f"[DEBUG] Hotel Detail Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"获取酒店详情失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/attraction/detail", methods=["POST"])
def get_attraction_detail():
    """
    景点详情接口
    
    获取特定景点的详细信息，包括开放时间、门票、简介等。
    
    请求参数（JSON）：
        name: 景点名称
        type: 类型（固定为 "attraction"）
        latitude: 纬度（可选）
        longitude: 经度（可选）
    """
    try:
        data = request.get_json()
        name = data.get("name", "")
        latitude = data.get("latitude", "")
        longitude = data.get("longitude", "")
        
        if not name:
            return make_response(status="error", message="景点名称不能为空", code="400")
        
        query = f"请查询景点【{name}】的详细信息，包括开放时间、门票、简介、游览建议等。坐标({latitude}, {longitude})。"
        result = attraction_detail_agent.run(query)
        result = extract_json(result)
        logger.info(f"[DEBUG] Attraction Detail Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"获取景点详情失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


@app.route("/api/restaurant/detail", methods=["POST"])
def get_restaurant_detail():
    """
    餐厅详情接口
    
    获取特定餐厅的详细信息，包括招牌菜、营业时间、人均消费等。
    
    请求参数（JSON）：
        name: 餐厅名称
        type: 类型（固定为 "restaurant"）
        latitude: 纬度（可选）
        longitude: 经度（可选）
    """
    try:
        data = request.get_json()
        name = data.get("name", "")
        latitude = data.get("latitude", "")
        longitude = data.get("longitude", "")
        
        if not name:
            return make_response(status="error", message="餐厅名称不能为空", code="400")
        
        query = f"请查询餐厅【{name}】的详细信息，包括招牌菜、营业时间、人均消费、联系方式等。坐标({latitude}, {longitude})。"
        result = restaurant_detail_agent.run(query)
        result = extract_json(result)
        logger.info(f"[DEBUG] Restaurant Detail Agent 原始返回: {result}")
        return make_response(status="success", message=result, code="200")
    except Exception as e:
        logger.error(f"获取餐厅详情失败: {str(e)}")
        return make_response(status="error", message=str(e), code="500")


# ==================== 应用入口 ====================

if __name__ == "__main__":
    """
    主程序入口
    
    启动 Flask 开发服务器，监听 0.0.0.0:8000
    可通过 http://localhost:8000 访问 API
    """
    app.run(host="0.0.0.0", port=8000, debug=True)
