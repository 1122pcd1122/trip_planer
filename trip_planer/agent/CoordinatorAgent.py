# -*- coding: utf-8 -*-
"""
CoordinatorAgent 协调 Agent 模块

作为智能旅行助手系统的"大脑"，负责统筹协调其他四个专项 Agent：
- 天气查询 Agent
- 景点推荐 Agent
- 酒店推荐 Agent
- 餐饮推荐 Agent

核心功能：
- 并发调度：使用 ThreadPoolExecutor 同时启动四个 Agent
- 行程规划：根据用户天数生成每天的详细行程安排
- 纯 JSON 输出：只输出 JSON，不包含任何解释性文字

工作流程：
    1. 并发调用四个专项 Agent 获取数据
    2. 收集所有返回结果
    3. 调用自身 LLM 能力生成详细行程
    4. 输出按天划分的旅行行程 JSON
"""

import concurrent.futures
import time
from trip_planer.agent.specific.WeatherAgent import WeatherAgent
from trip_planer.agent.specific.AttractionAgent import AttractionAgent
from trip_planer.agent.specific.HotelAgent import HotelAgent
from trip_planer.agent.specific.RestaurantAgent import RestaurantAgent
from trip_planer.agent.base.BaseAgent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """
    旅行计划协调 Agent（系统大脑）
    
    继承自 BaseAgent，是整个智能旅行助手系统的核心协调者。
    负责接收用户的旅行计划请求，统筹调度四个专项 Agent，
    并将返回的分散数据整合为详细的旅行行程安排。
    
    整合后的 JSON 结构：
        {
            "destination": "目的地",
            "days": [                  # 每天的行程安排
                {
                    "date": "日期",
                    "weather": "天气",
                    "morning": "上午安排",
                    "afternoon": "下午安排",
                    "evening": "晚上安排",
                    "hotel": "住宿推荐",
                    "tips": "当日建议"
                }
            ],
            "overallTips": "整体行程建议"
        }
    
    核心特性：
        - 并发执行：四个专项 Agent 同时运行，提高响应速度
        - 行程规划：根据天数生成每天的详细安排
        - 纯 JSON 输出：只输出 JSON，不包含任何解释性文字
        - 经纬度保留：有则保留，无则为空
    """

    def __init__(self):
        """
        初始化协调 Agent
        
        继承父类 BaseAgent 的初始化逻辑，设置特定的角色描述。
        同时实例化四个专项 Agent，用于后续的任务调度。
        
        角色描述要点：
            1. 明确职责：行程汇总整合
            2. 输出规范：纯 JSON，无解释、无 markdown、无注释
            3. 数据结构：固定字段 weatherInfo, spotInfo, hotelInfo, foodInfo, totalSummary
            4. 地理位置：必须保留 latitude（纬度）和 longitude（经度）
        """
        super().__init__(
            name="行程汇总Agent",
            role_description="你是专业旅行规划师，擅长制定完整旅行行程安排。"
                             "【核心任务】根据天气、景点、酒店、餐饮四类数据，生成按天划分的详细行程。"
                             "【输出规范】仅输出纯JSON，禁止解释、markdown。"
                             "【输出JSON格式】"
                             '{"days":[{"dayNum":1,"date":"2026-04-30","weather":"阴","itinerary":[{"time":"09:00","spot":"宽窄巷子","address":"成都市青羊区","latitude":"","longitude":""}],"meals":{"lunch":{"name":"","address":"","dish":""},"dinner":{"name":"","address":"","dish":""}},"tips":""}],"hotel":[{"name":"","address":"","price":"","advantage":"","latitude":"","longitude":""}],"overallTips":""}'
        )
        print("🤝 规划协调 Agent 正在集结它的专业团队...")
        
        # 实例化四个专项 Agent
        self.weather_agent = WeatherAgent()      # 天气查询 Agent
        self.attraction_agent = AttractionAgent()  # 景点推荐 Agent
        self.hotel_agent = HotelAgent()          # 酒店推荐 Agent
        self.restaurant_agent = RestaurantAgent()  # 餐饮推荐 Agent




    def generate_plan(self, destination: str, days: int, preferences: str = "") -> str:
        """
        生成旅行计划 - 非流式版本（推荐使用）
        
        并发调度四个专项 Agent，获取天气、景点、酒店、餐饮信息，
        然后调用自身 LLM 能力整合所有数据为统一的 JSON 格式。
        
        参数说明：
            destination: 目的地城市名称，如"成都"、"杭州"等
            days: 计划游玩天数，整数类型
            preferences: 用户偏好设置（可选），如"想吃火锅"、"想要海景房"等
        
        返回值：
            str: 整合后的旅行计划 JSON 字符串
        
        执行流程：
            ┌─────────────────────────────────────────┐
            │  1. 并发启动四个 Agent                  │
            │     - WeatherAgent                     │
            │     - AttractionAgent                  │
            │     - HotelAgent                       │
            │     - RestaurantAgent                 │
            └────────────────┬────────────────────────┘
                             ▼
            ┌─────────────────────────────────────────┐
            │  2. 等待所有 Agent 完成                 │
            │     - 收集 weather_info                │
            │     - 收集 attraction_info             │
            │     - 收集 hotel_info                  │
            │     - 收集 restaurant_info             │
            └────────────────┬────────────────────────┘
                             ▼
            ┌─────────────────────────────────────────┐
            │  3. 调用自身 LLM 整合数据               │
            │     - 构造整合 prompt                  │
            │     - 执行 run() 方法                   │
            │     - 输出统一 JSON                     │
            └─────────────────────────────────────────┘
        
        示例返回值：
            {
                "weatherInfo": {"temperature": "25°C", "condition": "晴"},
                "spotInfo": [{"name": "宽窄巷子", "latitude": 30.658, "longitude": 104.068}],
                "hotelInfo": [{"name": "成都香格里拉大酒店", "latitude": 30.652, "longitude": 104.071}],
                "foodInfo": [{"name": "小龙坎火锅", "latitude": 30.658, "longitude": 104.068}],
                "totalSummary": "成都3日游： Day1 游览宽窄巷子..."
            }
        """
        # 使用线程池并发执行四个 Agent
        # ThreadPoolExecutor 允许四个任务同时执行，大幅减少总等待时间
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            # 提交任务到线程池，立即返回 Future 对象
            future_weather = executor.submit(self.weather_agent.run, f"查询{destination}的天气情况，游玩{days}天。")
            future_attraction = executor.submit(self.attraction_agent.run,
                                                f"推荐{destination}的景点，游玩{days}天，偏好：{preferences}。")
            future_hotel = executor.submit(self.hotel_agent.run, f"推荐{destination}的酒店，游玩{days}天，偏好：{preferences}。")
            future_restaurant = executor.submit(self.restaurant_agent.run, f"推荐{destination}的特色餐饮，游玩{days}天，偏好：{preferences}。")

            # 等待所有任务完成并获取结果
            # result() 方法会阻塞直到任务完成
            weather_info = future_weather.result()
            attraction_info = future_attraction.result()
            hotel_info = future_hotel.result()
            restaurant_info = future_restaurant.result()

        # 构建整合提示词
        json_format = '{"days":[{"dayNum":1,"date":"2026-04-30","weather":"阴","itinerary":[{"time":"09:00","spot":"宽窄巷子","address":"成都市青羊区","latitude":"","longitude":""}],"meals":{"lunch":{"name":"","address":"","dish":""},"dinner":{"name":"","address":"","dish":""}},"tips":""}],"hotel":[{"name":"","address":"","price":"","advantage":"","latitude":"","longitude":""}],"overallTips":""}'
        
        synthesis_prompt = f"""
            根据以下信息生成{destination}{days}天详细旅行行程安排：
            【目的地】：{destination}
            【游玩天数】：{days}天
            【用户偏好】：{preferences if preferences else '无'}
            【天气】：{weather_info}
            【景点】：{attraction_info}
            【酒店】：{hotel_info}
            【美食】：{restaurant_info}
            
            返回格式（必须严格遵循）：
            {json_format}
            """
        
        # 调用父类的 run() 方法执行整合任务
        # 这里的 self 充当整合 Agent 的角色
        return self.run(synthesis_prompt)
