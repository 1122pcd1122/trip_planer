# -*- coding: utf-8 -*-
"""
Agent 管理器模块

提供统一的 Agent 生命周期管理，支持延迟加载和单例模式。
"""

from typing import Dict, Optional, Any
from trip_planer.util.logger import logger


class AgentManager:
    """
    Agent 管理器（单例模式）

    负责管理所有 Agent 的生命周期，实现延迟加载和统一管理。
    """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._agents = {}
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self._agents: Dict[str, Any] = {}
            self._initialized = True
            logger.info("✅ Agent 管理器初始化完成")

    def register_agent(self, name: str, agent: Any) -> None:
        """
        注册 Agent 实例

        参数：
            name: Agent 名称
            agent: Agent 实例
        """
        self._agents[name] = agent
        logger.info(f"✅ Agent [{name}] 已注册")

    def get_agent(self, name: str) -> Optional[Any]:
        """
        获取 Agent 实例

        参数：
            name: Agent 名称

        返回：
            Agent 实例，如果不存在返回 None
        """
        return self._agents.get(name)

    def has_agent(self, name: str) -> bool:
        """
        检查 Agent 是否已注册

        参数：
            name: Agent 名称

        返回：
            布尔值
        """
        return name in self._agents

    def list_agents(self) -> list:
        """
        获取所有已注册的 Agent 名称列表

        返回：
            Agent 名称列表
        """
        return list(self._agents.keys())

    def clear_agents(self) -> None:
        """
        清除所有 Agent 实例，释放资源
        """
        self._agents.clear()
        logger.info("🗑️ 所有 Agent 实例已清除")

    def create_weather_agent(self):
        """创建并注册天气 Agent"""
        from trip_planer.agent.specific.WeatherAgent import WeatherAgent
        weather_agent = WeatherAgent()
        self.register_agent("weather", weather_agent)
        return weather_agent

    def create_attraction_agent(self):
        """创建并注册景点 Agent"""
        from trip_planer.agent.specific.AttractionAgent import AttractionAgent
        attraction_agent = AttractionAgent()
        self.register_agent("attraction", attraction_agent)
        return attraction_agent

    def create_hotel_agent(self):
        """创建并注册酒店 Agent"""
        from trip_planer.agent.specific.HotelAgent import HotelAgent
        hotel_agent = HotelAgent()
        self.register_agent("hotel", hotel_agent)
        return hotel_agent

    def create_restaurant_agent(self):
        """创建并注册餐厅 Agent"""
        from trip_planer.agent.specific.RestaurantAgent import RestaurantAgent
        restaurant_agent = RestaurantAgent()
        self.register_agent("restaurant", restaurant_agent)
        return restaurant_agent

    def create_coordinator_agent(self):
        """创建并注册协调 Agent"""
        from trip_planer.agent.CoordinatorAgent import CoordinatorAgent
        coordinator_agent = CoordinatorAgent()
        self.register_agent("coordinator", coordinator_agent)
        return coordinator_agent

    def create_hotel_detail_agent(self):
        """创建并注册酒店详情 Agent"""
        from trip_planer.agent.specific.HotelDetailAgent import HotelDetailAgent
        hotel_detail_agent = HotelDetailAgent()
        self.register_agent("hotel_detail", hotel_detail_agent)
        return hotel_detail_agent

    def create_attraction_detail_agent(self):
        """创建并注册景点详情 Agent"""
        from trip_planer.agent.specific.AttractionDetailAgent import AttractionDetailAgent
        attraction_detail_agent = AttractionDetailAgent()
        self.register_agent("attraction_detail", attraction_detail_agent)
        return attraction_detail_agent

    def create_restaurant_detail_agent(self):
        """创建并注册餐厅详情 Agent"""
        from trip_planer.agent.specific.RestaurantDetailAgent import RestaurantDetailAgent
        restaurant_detail_agent = RestaurantDetailAgent()
        self.register_agent("restaurant_detail", restaurant_detail_agent)
        return restaurant_detail_agent

    def get_or_create_agent(self, name: str) -> Optional[Any]:
        """
        获取或创建 Agent

        参数：
            name: Agent 名称

        返回：
            Agent 实例
        """
        if self.has_agent(name):
            return self.get_agent(name)

        creator_method = getattr(self, f"create_{name}_agent", None)
        if creator_method:
            return creator_method()

        logger.warning(f"⚠️ 未找到 Agent 创建方法: {name}")
        return None

    def initialize_all_agents(self) -> None:
        """
        初始化所有预定义的 Agent

        通常在应用启动时调用一次，避免延迟加载带来的首次请求慢问题。
        """
        logger.info("🚀 正在初始化所有 Agent...")

        self.create_weather_agent()
        self.create_attraction_agent()
        self.create_hotel_agent()
        self.create_restaurant_agent()
        self.create_coordinator_agent()
        self.create_hotel_detail_agent()
        self.create_attraction_detail_agent()
        self.create_restaurant_detail_agent()

        logger.info("✅ 所有 Agent 初始化完成")


agent_manager = AgentManager()