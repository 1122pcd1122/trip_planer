# -*- coding: utf-8 -*-
"""
WeatherAgent 天气查询 Agent 模块

继承自 BaseAgent，专门负责天气信息查询功能。
通过调用和风天气 API 获取目的地的天气预报数据。

主要功能：
- 多天天气预报查询
- 温度、天气状况获取
- 个性化出行建议生成

使用示例：
    from trip_planer.agent.specific.WeatherAgent import WeatherAgent
    
    agent = WeatherAgent()
    result = agent.run("查询成都的天气，游玩3天")
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.WeatherService import weather_service
from trip_planer.util.logger import logger


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

    def run(self, user_input: str) -> str:
        """
        重写 run 方法，直接使用和风天气 API，不经过 LLM。
        
        参数说明：
            user_input: 用户输入，包含城市名和天数信息
        
        返回值：
            str: JSON 格式的天气数据
        """
        logger.info(f"\n[{self.name}] 收到任务: {user_input}")

        # 从用户输入中解析城市名和天数
        city_name = self._parse_city_name(user_input)
        days = self._parse_days(user_input)

        if not city_name:
            return '{"error": "无法解析城市名，请检查输入"}'

        logger.info(f"🌤️ 正在查询 [{city_name}] 的天气，共 {days} 天...")

        # 调用和风天气服务
        result = weather_service.get_weather_forecast(city_name, days)

        if "error" in result:
            return f'{{"error": "{result["error"]}"}}'

        # 将结果转换为 JSON 字符串
        import json
        return json.dumps(result, ensure_ascii=False)

    def _parse_city_name(self, text: str) -> str:
        """
        从文本中解析城市名
        
        参数说明：
            text: 用户输入文本
        
        返回值：
            str: 城市名，未找到则返回空字符串
        """
        # 支持多种格式：
        # - "查询 成都 的天气"
        # - "成都 天气"
        # - "查询成都天气"
        import re

        # 提取中文字符串作为城市名
        patterns = [
            r'查询\s*([\u4e00-\u9fa5]+?)\s*的天气',
            r'([\u4e00-\u9fa5]+?)\s*天气',
            r'查询\s*([\u4e00-\u9fa5]+?)\s*',
        ]

        for pattern in patterns:
            match = re.search(pattern, text)
            if match:
                return match.group(1)

        return ""

    def _parse_days(self, text: str) -> int:
        """
        从文本中解析天数
        
        参数说明：
            text: 用户输入文本
        
        返回值：
            int: 天数，默认 3 天
        """
        import re

        # 提取数字
        match = re.search(r'(\d+)\s*天', text)
        if match:
            return int(match.group(1))

        return 3  # 默认查询 3 天
