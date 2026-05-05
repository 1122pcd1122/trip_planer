# -*- coding: utf-8 -*-
"""
CoordinatorAgent 协调 Agent 模块

作为智能旅行助手系统的"大脑"，负责统筹协调其他四个专项 Agent。
核心功能：并发调度、行程规划、容错处理、纯 JSON 输出。
"""

import concurrent.futures
import logging
from trip_planer.agent.specific.WeatherAgent import WeatherAgent
from trip_planer.agent.specific.AttractionAgent import AttractionAgent
from trip_planer.agent.specific.HotelAgent import HotelAgent
from trip_planer.agent.specific.RestaurantAgent import RestaurantAgent
from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.util.logger import logger


class CoordinatorAgent(BaseAgent):
    """旅行计划协调 Agent（系统大脑）"""

    def __init__(self):
        super().__init__(
            name="行程汇总Agent",
            role_description=(
                "你是专业旅行规划师。根据天气、景点、酒店、餐饮数据，生成按天划分的详细行程。\n"
                "【规则】直接输出纯JSON，禁止解释、markdown。\n"
                "【JSON格式】\n"
                '{"days":[{"dayNum":1,"date":"2026-04-30","weather":"阴","itinerary":[{"time":"09:00","spot":"宽窄巷子","address":"成都市青羊区","latitude":"","longitude":""}],"meals":{"lunch":{"name":"","address":"","dish":""},"dinner":{"name":"","address":"","dish":""}},"tips":""}],"hotel":[{"name":"","address":"","price":"","advantage":"","latitude":"","longitude":""}],"overallTips":""}'
            )
        )
        logger.info("🤝 规划协调 Agent 正在集结专业团队...")
        
        self.weather_agent = WeatherAgent()
        self.attraction_agent = AttractionAgent()
        self.hotel_agent = HotelAgent()
        self.restaurant_agent = RestaurantAgent()

    def _safe_run_agent(self, agent, query: str, agent_name: str) -> str:
        """安全运行单个 Agent，失败时返回空数据"""
        try:
            result = agent.run(query)
            if result and len(result.strip()) > 0:
                logger.info(f"✅ {agent_name} 返回成功")
                return result
            else:
                logger.warning(f"⚠️ {agent_name} 返回空数据")
                return "{}"
        except Exception as e:
            logger.error(f"❌ {agent_name} 失败: {str(e)}")
            return "{}"

    def generate_plan(self, destination: str, days: int, preferences: str = "") -> str:
        """
        生成旅行计划（带容错机制）
        
        单个 Agent 失败不影响整体行程生成。
        """
        json_format = (
            '{"days":[{"dayNum":1,"date":"2026-04-30","weather":"阴",'
            '"itinerary":[{"time":"09:00","spot":"宽窄巷子","address":"成都市青羊区",'
            '"latitude":"","longitude":""}],"meals":{"lunch":{"name":"","address":"","dish":""},'
            '"dinner":{"name":"","address":"","dish":""}},"tips":""}],'
            '"hotel":[{"name":"","address":"","price":"","advantage":"","latitude":"","longitude":""}],'
            '"overallTips":""}'
        )
        
        pref_note = ""
        if preferences:
            pref_note = f"\n【用户偏好标签】：{preferences}\n请根据这些偏好标签精准推荐（如酒店档次、餐饮类型、景点类型等）。"
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            future_weather = executor.submit(
                self._safe_run_agent, 
                self.weather_agent, 
                f"查询{destination}的天气情况，游玩{days}天。{pref_note}",
                "天气Agent"
            )
            future_attraction = executor.submit(
                self._safe_run_agent,
                self.attraction_agent,
                f"推荐{destination}的景点，游玩{days}天。{pref_note}",
                "景点Agent"
            )
            future_hotel = executor.submit(
                self._safe_run_agent,
                self.hotel_agent,
                f"推荐{destination}的酒店，游玩{days}天。{pref_note}",
                "酒店Agent"
            )
            future_restaurant = executor.submit(
                self._safe_run_agent,
                self.restaurant_agent,
                f"推荐{destination}的特色餐饮，游玩{days}天。{pref_note}",
                "餐饮Agent"
            )

            weather_info = future_weather.result()
            attraction_info = future_attraction.result()
            hotel_info = future_hotel.result()
            restaurant_info = future_restaurant.result()

        synthesis_prompt = (
            f"根据以下信息生成{destination}{days}天详细旅行行程安排：\n"
            f"【目的地】：{destination}\n"
            f"【游玩天数】：{days}天\n"
            f"【用户偏好】：{preferences if preferences else '无'}\n"
            f"【天气】：{weather_info}\n"
            f"【景点】：{attraction_info}\n"
            f"【酒店】：{hotel_info}\n"
            f"【美食】：{restaurant_info}\n\n"
            f"返回格式（必须严格遵循）：\n{json_format}"
        )
        
        return self.run(synthesis_prompt)
