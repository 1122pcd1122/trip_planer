# -*- coding: utf-8 -*-
"""
WeatherAgent 天气查询 Agent 模块

继承自 BaseAgent，专门负责天气信息查询功能。
通过调用高德地图 API 获取目的地的实时天气和未来预报数据。
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class WeatherAgent(BaseAgent):
    """天气查询 Agent"""

    def __init__(self):
        super().__init__(
            name="天气查询专家",
            role_description=(
                "你是气象数据分析师。根据用户输入的城市和天数，查询天气并输出JSON。\n"
                "【规则】\n"
                "1. 直接输出纯JSON，禁止任何解释、markdown、前后缀\n"
                "2. 根据天数返回对应天数的天气数据\n"
                "3. 结合天气给出针对性出行建议\n"
                "【JSON格式】\n"
                "{\"weatherList\":[{\"cityName\":\"城市名\",\"latitude\":\"\",\"longitude\":\"\",\"date\":\"YYYY-MM-DD\",\"weather\":\"晴/多云/雨\",\"temperature\":\"23℃\",\"tips\":\"出行建议\"}]}"
            )
        )
        self.equip_tool(tool_manager.get_amap_tools())
