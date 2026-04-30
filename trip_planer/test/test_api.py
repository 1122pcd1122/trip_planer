import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"


def test_health_check():
    """测试根目录健康检查接口"""
    print("=========================================")
    print("1. 测试健康检查接口 (GET /)")
    print("=========================================")
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"返回结果: {response.json()}\n")
    except Exception as e:
        print(f"❌ 连接失败，请确认 FastAPI 服务器是否已启动！报错: {e}\n")


def test_stream_plan():
    """测试汇总Agent接口"""
    print("=========================================")
    print("2. 测试汇总Agent接口 (POST /api/plan/stream)")
    print("=========================================")
    payload = {
        "destination": "成都",
        "days": 2,
        "preferences": "和女朋友"
    }

    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/plan/stream", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_weather_agent():
    """测试天气Agent接口"""
    print("\n=========================================")
    print("3. 测试天气Agent接口 (POST /api/weather)")
    print("=========================================")
    payload = {"destination": "成都"}
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/weather", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_attraction_agent():
    """测试景点Agent接口"""
    print("\n=========================================")
    print("4. 测试景点Agent接口 (POST /api/attraction)")
    print("=========================================")
    payload = {"destination": "成都"}
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/attraction", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_hotel_agent():
    """测试酒店Agent接口"""
    print("\n=========================================")
    print("5. 测试酒店Agent接口 (POST /api/hotel)")
    print("=========================================")
    payload = {"destination": "成都"}
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/hotel", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


def test_restaurant_agent():
    """测试餐饮Agent接口"""
    print("\n=========================================")
    print("6. 测试餐饮Agent接口 (POST /api/restaurant)")
    print("=========================================")
    payload = {"destination": "成都"}
    print(f"正在发送请求: {payload}")
    response = requests.post(f"{BASE_URL}/api/restaurant", json=payload)
    print(f"状态码: {response.status_code}")
    result = response.json()
    print(f"返回结果: {result}\n")


if __name__ == "__main__":
    test_health_check()
    test_weather_agent()
    test_attraction_agent()
    test_hotel_agent()
    test_restaurant_agent()
    test_stream_plan()
