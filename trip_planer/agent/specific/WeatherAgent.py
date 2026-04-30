# -*- coding: utf-8 -*-
"""
WeatherAgent 天气查询 Agent 模块

继承自 BaseAgent，专门负责天气信息查询功能。
通过调用高德地图 API 获取目的地的实时天气和未来预报数据。

主要功能：
- 实时天气查询：获取当前城市的气温、天气状态、风力等信息
- 出行建议：根据天气情况提供穿衣、防晒、防雨等建议
- 地理位置信息：返回城市的经纬度坐标

输出格式：纯 JSON 字符串，包含 cityName、latitude、longitude、date、weather、temperature、tips 等字段
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class WeatherAgent(BaseAgent):
    """
    天气查询 Agent
    
    继承自 BaseAgent，专门用于处理天气查询请求。
    装配高德地图工具，通过调用外部 API 获取天气数据。
    
    核心职责：
        - 接收天气查询请求
        - 调用高德地图天气 API
        - 解析返回的天气数据
        - 生成符合规范的 JSON 格式输出
    
    输出 JSON 字段说明：
        - cityName: 城市名称
        - latitude: 城市纬度
        - longitude: 城市经度
        - date: 查询日期
        - weather: 天气状态（如"晴"、"多云"、"小雨"等）
        - temperature: 温度（如"25°C"、"18~22°C"等）
        - tips: 出行建议（如"建议带伞"、"注意防晒"等）
    """

    def __init__(self):
        """
        初始化天气查询 Agent
        
        设置 Agent 名称和角色描述，同时装配高德地图工具。
        
        角色描述要点：
            - 专业定位：天气推荐专家
            - 查询内容：实时天气、温度、风力、降水概率、空气质量、未来预报
            - 附加服务：出行穿搭、防晒、防雨等实用提示
        
        输出规范（强制规则）：
            1. 仅输出纯 JSON 字符串，不包含任何其他内容
            2. 禁止输出 markdown 代码块标记（如 ```json ```）
            3. 禁止输出任何解释、说明、前缀文字
            4. 直接输出 JSON 对象，不需要任何包装
        """
        super().__init__(
            name="天气查询专家",
            role_description=""
                             "你是专业气象数据分析师，精通天气分析与出行建议。用户输入目的地城市和游玩天数后，你必须："
                             "1. 使用高德地图API查询该城市实时天气数据（气温、天气状态、风力、空气质量）"
                             "2. 【关键】根据用户游玩天数，提供未来N天的天气预报"
                             "   - 用户游玩1天 → 返回1天数据"
                             "   - 用户游玩2天 → 返回2天数据"
                             "   - 用户游玩3天 → 返回3天数据"
                             "   - 以此类推..."
                             "3. 结合每天的天气情况，给出针对性的出行建议（穿衣、防晒、防雨、防寒等）"
                             ""
                             "【核心任务】"
                             "- 接收城市名称和天数 → 调用天气工具 → 直接输出JSON"
                             "- 如用户有特殊偏好（如看雪山、户外活动），需在建议中体现"
                             ""
                             "【强制输出规则】"
                             "1. 直接输出JSON，不要有任何思考过程、解释文字"
                             "2. 仅输出纯JSON字符串，禁止任何解释、前缀、后缀"
                             "3. 禁止使用markdown代码块标记"
                             "4. JSON必须使用数组格式weatherList，包含多天数据"
                             "5. weatherList中每个元素包含：cityName, latitude, longitude, date, weather, temperature, tips（如无经纬度则为空字符串）"
                             ""
                             "【输出JSON格式】"
                             "{\"weatherList\":[{\"cityName\":\"成都市\",\"latitude\":\"\",\"longitude\":\"\",\"date\":\"2026-04-30\",\"weather\":\"阴\",\"temperature\":\"23℃\",\"tips\":\"建议\"}]}"
        )
        # 装配高德地图工具，获取天气查询能力
        self.equip_tool(tool_manager.get_amap_tools())
