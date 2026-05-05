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
- 酒店详情接口
- 景点详情接口
- 餐厅详情接口

使用说明：
1. 先启动 Flask 服务器 (python main_api.py)
2. 运行本测试文件 (python -m trip_planer.test.test_api)
"""

import requests
import json
import time

# 测试服务器基础 URL，指向本地 Flask 服务
BASE_URL = "http://127.0.0.1:8000"

# 统一的 API 响应格式
# {
#     "status": "success" | "error",
#     "message": "响应内容（JSON字符串）",
#     "code": "200" | "500"
# }


def test_health_check():
    """
    测试健康检查接口

    用途：验证服务器是否正常运行
    接口：GET /
    预期：返回 {"status": "ok", "message": "Welcome...", "code": "200"}
    """
    print("=" * 50)
    print("1. 测试健康检查接口 (GET /)")
    print("=" * 50)
    try:
        response = requests.get(f"{BASE_URL}/")
        print(f"状态码: {response.status_code}")
        print(f"返回结果: {json.dumps(response.json(), ensure_ascii=False, indent=2)}\n")
    except Exception as e:
        print(f"❌ 连接失败，请确认 Flask 服务器是否已启动！报错: {e}\n")


def test_plan():
    """
    测试生成旅行计划接口

    用途：测试协调 Agent 是否能正确调用各专项 Agent 并汇总结果
    接口：POST /api/plan
    请求参数：
        - destination: 目的地城市
        - days: 旅行天数（字符串格式）
        - preferences: 用户偏好/特殊要求
    预期：返回包含天气、景点、酒店、餐饮的完整旅行计划
    """
    print("=" * 50)
    print("2. 测试生成旅行计划接口 (POST /api/plan)")
    print("=" * 50)
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": "和女朋友"
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/plan", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:200]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


def test_weather_agent():
    """
    测试天气查询 Agent 接口

    用途：验证天气 Agent 能否正确查询指定城市的天气信息
    接口：POST /api/weather
    请求参数：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含温度、天气状况、建议等信息的 JSON
    """
    print("=" * 50)
    print("3. 测试天气Agent接口 (POST /api/weather)")
    print("=" * 50)
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/weather", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:200]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


def test_attraction_agent():
    """
    测试景点推荐 Agent 接口

    用途：验证景点 Agent 能否正确推荐指定城市的热门景点
    接口：POST /api/attraction
    请求参数：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含景点名称、地址、评分、开放时间等信息的 JSON 列表
    """
    print("=" * 50)
    print("4. 测试景点Agent接口 (POST /api/attraction)")
    print("=" * 50)
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/attraction", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:200]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


def test_hotel_agent():
    """
    测试酒店推荐 Agent 接口

    用途：验证酒店 Agent 能否正确推荐指定城市的优质酒店
    接口：POST /api/hotel
    请求参数：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含酒店名称、地址、星级、价格区间等信息的 JSON 列表
    """
    print("=" * 50)
    print("5. 测试酒店Agent接口 (POST /api/hotel)")
    print("=" * 50)
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/hotel", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:200]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


def test_restaurant_agent():
    """
    测试餐饮推荐 Agent 接口

    用途：验证餐饮 Agent 能否正确推荐指定城市的特色餐厅
    接口：POST /api/restaurant
    请求参数：
        - destination: 目的地城市
        - days: 旅行天数（可选）
        - preferences: 用户偏好（可选）
    预期：返回包含餐厅名称、地址、菜系、评分等信息的 JSON 列表
    """
    print("=" * 50)
    print("6. 测试餐饮Agent接口 (POST /api/restaurant)")
    print("=" * 50)
    payload = {
        "destination": "成都",
        "days": "2",
        "preferences": ""
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/restaurant", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:200]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


def test_hotel_detail():
    """
    测试酒店详情接口

    用途：验证能否获取特定酒店的详细信息
    接口：POST /api/hotel/detail
    请求参数：
        - name: 酒店名称
        - type: 类型（固定为 "hotel"）
        - latitude: 纬度（可选）
        - longitude: 经度（可选）
    预期：返回包含酒店设施、房型、评分、联系方式等详细信息的 JSON
    """
    print("=" * 50)
    print("7. 测试酒店详情接口 (POST /api/hotel/detail)")
    print("=" * 50)
    payload = {
        "name": "成都香格里拉大酒店",
        "type": "hotel",
        "latitude": "30.65",
        "longitude": "104.07"
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/hotel/detail", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:300]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


def test_attraction_detail():
    """
    测试景点详情接口

    用途：验证能否获取特定景点的详细信息
    接口：POST /api/attraction/detail
    请求参数：
        - name: 景点名称
        - type: 类型（固定为 "attraction"）
        - latitude: 纬度（可选）
        - longitude: 经度（可选）
    预期：返回包含景点开放时间、门票价格、简介、游览建议等信息的 JSON
    """
    print("=" * 50)
    print("8. 测试景点详情接口 (POST /api/attraction/detail)")
    print("=" * 50)
    payload = {
        "name": "武侯祠",
        "type": "attraction",
        "latitude": "30.64",
        "longitude": "104.05"
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/attraction/detail", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:300]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


def test_restaurant_detail():
    """
    测试餐厅详情接口

    用途：验证能否获取特定餐厅的详细信息
    接口：POST /api/restaurant/detail
    请求参数：
        - name: 餐厅名称
        - type: 类型（固定为 "restaurant"）
        - latitude: 纬度（可选）
        - longitude: 经度（可选）
    预期：返回包含餐厅招牌菜、营业时间、人均消费、联系方式等信息的 JSON
    """
    print("=" * 50)
    print("9. 测试餐厅详情接口 (POST /api/restaurant/detail)")
    print("=" * 50)
    payload = {
        "name": "小龙坎火锅",
        "type": "restaurant",
        "latitude": "30.65",
        "longitude": "104.07"
    }
    print(f"正在发送请求: {json.dumps(payload, ensure_ascii=False)}")
    try:
        response = requests.post(f"{BASE_URL}/api/restaurant/detail", json=payload)
        print(f"状态码: {response.status_code}")
        result = response.json()
        print(f"返回状态: {result.get('status')}")
        print(f"返回消息: {result.get('message')[:300]}...\n")
    except Exception as e:
        print(f"❌ 请求失败: {e}\n")


if __name__ == "__main__":
    """
    主测试入口

    测试执行顺序：
    1. 健康检查 - 确保服务器可用
    2. 旅行计划 - 验证多 Agent 协调能力
    3-6. 各专项 Agent 测试 - 验证独立服务
    7-9. 详情接口测试 - 验证详情查询功能

    注意：测试会按顺序执行，可能耗时较长（每次请求需等待 LLM 响应）
    """
    print("\n🚀 开始测试 Flask API 接口...\n")
    
    test_health_check()
    
    print("\n请选择要测试的接口（输入数字，多个用逗号分隔，如 1,2,3）：")
    print("1. 旅行计划生成")
    print("2. 天气查询")
    print("3. 景点推荐")
    print("4. 酒店推荐")
    print("5. 餐饮推荐")
    print("6. 酒店详情")
    print("7. 景点详情")
    print("8. 餐厅详情")
    print("9. 全部测试")
    print("0. 退出")
    
    choice = input("\n请输入选择: ").strip()
    
    if choice == "0":
        print("退出测试")
        exit()
    
    if choice == "9":
        test_plan()
        time.sleep(1)
        test_weather_agent()
        time.sleep(1)
        test_attraction_agent()
        time.sleep(1)
        test_hotel_agent()
        time.sleep(1)
        test_restaurant_agent()
        time.sleep(1)
        test_hotel_detail()
        time.sleep(1)
        test_attraction_detail()
        time.sleep(1)
        test_restaurant_detail()
    else:
        choices = [c.strip() for c in choice.split(",")]
        for c in choices:
            if c == "1":
                test_plan()
            elif c == "2":
                test_weather_agent()
            elif c == "3":
                test_attraction_agent()
            elif c == "4":
                test_hotel_agent()
            elif c == "5":
                test_restaurant_agent()
            elif c == "6":
                test_hotel_detail()
            elif c == "7":
                test_attraction_detail()
            elif c == "8":
                test_restaurant_detail()
            else:
                print(f"无效选择: {c}")
            time.sleep(1)
    
    print("\n✅ 测试完成！")
