"""
API 接口测试模块

本模块提供对所有后端 API 接口的手动测试功能
用于验证各 Agent 服务的正确性和响应格式

测试对象：
- 健康检查接口
- 旅行计划生成接口
- 天气查询 Agent
- 景点推荐 Agent
- 酒店推荐 Agent
- 餐饮推荐 Agent

使用说明：
1. 先启动 FastAPI 服务器 (uvicorn main_api:app --reload)
2. 运行本测试文件 (python -m trip_planer.test.test_api)
"""

import requests
import json
import time

# 测试服务器基础 URL，指向本地 FastAPI 服务
BASE_URL = "http://127.0.0.1:8000"

# 测试请求参数 - 统一的 TripPlanRequest 格式
TEST_PAYLOAD = {
    "destination": "成都",
    "days": "2",
    "preferences": "和女朋友"
}


def test_health_check():
    """
    测试根目录健康检查接口

    用途：验证服务器是否正常运行
    接口：GET /
    预期：返回包含服务器状态的基本信息
    """
    print("=========================================")
    print("1. 测试健康检查接口 (GET /)")
    print("=========================================")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"返回结果: {response.json()}\n")
    except Exception as e:
        print(f"❌ 连接失败，请确认 FastAPI 服务器是否已启动！报错: {e}\n")


def test_plan():
    """
    测试生成旅行计划接口

    用途：测试协调 Agent 是否能正确调用各专项 Agent 并汇总结果
    接口：POST /api/plan
    请求参数（TripPlanRequest）：
        - destination: 目的地城市
        - days: 旅行天数（字符串格式）
        - preferences: 用户偏好/特殊要求
    预期：返回包含天气、景点、酒店、餐饮的完整旅行计划
    """
    print("=========================================")
    print("2. 测试生成旅行计划接口 (POST /api/plan)")
    print("=========================================")
    print(f"正在发送请求: {TEST_PAYLOAD}")
    response = requests.post(f"{BASE_URL}/api/plan", json=TEST_PAYLOAD)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_weather_agent():
    """
    测试天气查询 Agent 接口

    用途：验证天气 Agent 能否正确查询指定城市的天气信息
    接口：POST /api/weather
    请求参数（TripPlanRequest）：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含温度、天气状况、建议等信息的 JSON
    """
    print("\n=========================================")
    print("3. 测试天气Agent接口 (POST /api/weather)")
    print("=========================================")
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/weather", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_attraction_agent():
    """
    测试景点推荐 Agent 接口

    用途：验证景点 Agent 能否正确推荐指定城市的热门景点
    接口：POST /api/attraction
    请求参数（TripPlanRequest）：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含景点名称、地址、评分、开放时间等信息的 JSON 列表
    """
    print("\n=========================================")
    print("4. 测试景点Agent接口 (POST /api/attraction)")
    print("=========================================")
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/attraction", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_hotel_agent():
    """
    测试酒店推荐 Agent 接口

    用途：验证酒店 Agent 能否正确推荐指定城市的优质酒店
    接口：POST /api/hotel
    请求参数（TripPlanRequest）：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含酒店名称、地址、星级、价格区间等信息的 JSON 列表
    """
    print("\n=========================================")
    print("5. 测试酒店Agent接口 (POST /api/hotel)")
    print("=========================================")
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/hotel", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_restaurant_agent():
    """
    测试餐饮推荐 Agent 接口

    用途：验证餐饮 Agent 能否正确推荐指定城市的特色餐厅
    接口：POST /api/restaurant
    请求参数（TripPlanRequest）：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含餐厅名称、地址、菜系、评分等信息的 JSON 列表
    """
    print("\n=========================================")
    print("6. 测试餐饮Agent接口 (POST /api/restaurant)")
    print("=========================================")
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/restaurant", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


if __name__ == "__main__":
    """
    主测试入口

    测试执行顺序：
    1. 健康检查 - 确保服务器可用
    2. 旅行计划 - 验证多 Agent 协调能力
    3-6. 各专项 Agent 测试 - 验证独立服务

    注意：测试会按顺序执行，可能耗时较长（每次请求需等待 LLM 响应）
    """
    test_health_check()
    # test_plan()
    test_weather_agent()
    # test_attraction_agent()
    # test_hotel_agent()
    # test_restaurant_agent()
