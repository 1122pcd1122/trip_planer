# trip_planer/agent/CoordinatorAgent.py

import concurrent.futures
import time
from trip_planer.agent.specific.WeatherAgent import WeatherAgent
from trip_planer.agent.specific.AttractionAgent import AttractionAgent
from trip_planer.agent.specific.HotelAgent import HotelAgent
from trip_planer.agent.specific.RestaurantAgent import RestaurantAgent
from trip_planer.agent.base.BaseAgent import BaseAgent


class CoordinatorAgent(BaseAgent):
    """
    规划协调 Agent (系统大脑)
    负责统筹调用天气、景点、酒店、饭店四个专项Agent，并整合为纯JSON输出
    """

    def __init__(self):
        super().__init__(
            name="行程汇总Agent",
            role_description="你是行程汇总整合Agent。"
                             "接收天气、景点、酒店、饭店四类JSON数据，整合为统一简洁JSON，保留全部经纬度，遵守全局规则："
                             "1. 仅输出纯JSON，无解释、无多余文字、无markdown、无注释 "
                             "2. 地理位置固定字段：latitude(纬度)、longitude(经度)。输出结构：{weatherInfo, spotInfo, hotelInfo, foodInfo, totalSummary}"
        )
        print("🤝 规划协调 Agent 正在集结它的专业团队...")
        self.weather_agent = WeatherAgent()
        self.attraction_agent = AttractionAgent()
        self.hotel_agent = HotelAgent()
        self.restaurant_agent = RestaurantAgent()

    def generate_plan_stream(self, destination: str, days: int, preferences: str = ""):
        """
        4个Agent并发调度 + 汇总Agent整合
        """
        yield "🤖[系统] 正在唤醒规划中枢...\n"
        time.sleep(0.2)
        yield "⚡[系统] 启动多线程引擎，同时指派四大管家搜集情报...\n\n"

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_weather = executor.submit(self.weather_agent.run, f"请查询 {destination} 的天气情况。")
            future_attraction = executor.submit(self.attraction_agent.run,
                                                f"用户要在 {destination} 玩 {days} 天，偏好是：{preferences}。请推荐合适的景点。")
            future_hotel = executor.submit(self.hotel_agent.run, f"请在 {destination} 推荐几家交通便利的优质住宿。")
            future_restaurant = executor.submit(self.restaurant_agent.run, f"请在 {destination} 推荐本地特色餐饮。")

            weather_info = future_weather.result()
            yield "✅[天气管家] 汇报完毕！\n"

            attraction_info = future_attraction.result()
            yield "✅[景点管家] 汇报完毕！\n"

            hotel_info = future_hotel.result()
            yield "✅[酒店管家] 汇报完毕！\n"

            restaurant_info = future_restaurant.result()
            yield "✅[美食管家] 汇报完毕！\n\n"

        yield "🧠[系统] 外部数据全部集齐！开始汇总整合...\n\n---\n\n"

        synthesis_prompt = f"""
            整合以下四类JSON数据为统一纯JSON输出：
            【天气】：{weather_info}
            【景点】：{attraction_info}
            【酒店】：{hotel_info}
            【美食】：{restaurant_info}
            
            必须保留全部经纬度信息，输出格式：
            {{"weatherInfo":{{...}}, "spotInfo":{{...}}, "hotelInfo":{{...}}, "foodInfo":{{...}}, "totalSummary":"行程简要总结"}}
            只输出纯JSON，禁止任何多余文字。
            """

        for chunk in self.run_stream(synthesis_prompt):
            yield chunk

    def generate_plan(self, destination: str, days: int, preferences: str = ""):
        """
        非流式版本：4个Agent并发调度 + 汇总Agent整合
        """
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_weather = executor.submit(self.weather_agent.run, f"请查询 {destination} 的天气情况。")
            future_attraction = executor.submit(self.attraction_agent.run,
                                                f"用户要在 {destination} 玩 {days} 天，偏好是：{preferences}。请推荐合适的景点。")
            future_hotel = executor.submit(self.hotel_agent.run, f"请在 {destination} 推荐几家交通便利的优质住宿。")
            future_restaurant = executor.submit(self.restaurant_agent.run, f"请在 {destination} 推荐本地特色餐饮。")

            weather_info = future_weather.result()
            attraction_info = future_attraction.result()
            hotel_info = future_hotel.result()
            restaurant_info = future_restaurant.result()

        synthesis_prompt = f"""
            整合以下四类JSON数据为统一纯JSON输出：
            【天气】：{weather_info}
            【景点】：{attraction_info}
            【酒店】：{hotel_info}
            【美食】：{restaurant_info}

            必须保留全部经纬度信息，输出格式：
            {{"weatherInfo":{{...}}, "spotInfo":{{...}}, "hotelInfo":{{...}}, "foodInfo":{{...}}, "totalSummary":"行程简要总结"}}
            只输出纯JSON，禁止任何多余文字。
            """
        return self.run(synthesis_prompt)