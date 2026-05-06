# -*- coding: utf-8 -*-
"""
AttractionAgent 景点推荐 Agent 模块

继承自 BaseAgent，专门负责景点推荐功能。
通过调用高德地图 API 获取目的地的热门景点信息。

主要功能：
- 根据城市、天数、偏好推荐景点
- 返回景点详细信息（名称、坐标、地址、评分、简介、门票、开放时等）
- 支持多维度标签筛选（类型、场景、强度、预算）

使用示例：
    from trip_planer.agent.specific.AttractionAgent import AttractionAgent
    
    agent = AttractionAgent()
    result = agent.run("推荐 成都 的景点，游玩3天，偏好自然风光，预算100-200元")
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class AttractionAgent(BaseAgent):
    """景点推荐 Agent"""

    def __init__(self):
        super().__init__(
            name="景点推荐Agent",
            role_description=(
                "你是资深旅行策划师。根据用户输入的城市、天数和偏好标签，推荐景点并输出JSON。\n"
                "【规则】\n"
                "1. 直接输出纯JSON，禁止任何解释、markdown、前后缀\n"
                "2. 根据天数合理推荐数量：1-2天推荐3-5个，3-5天推荐6-10个，5天以上推荐8-12个\n"
                "3. 【关键】根据用户偏好标签精准匹配：\n"
                "   - 类型标签：自然风光、人文古迹、主题乐园、博物馆、历史遗迹、宗教寺庙、现代建筑\n"
                "   - 场景标签：亲子游(适合儿童)、情侣约会(浪漫)、拍照打卡(网红)、独自一人(安静)\n"
                "   - 强度标签：轻松休闲(步行即可)、中等强度(需少量步行)、体力挑战(登山/徒步)\n"
                "   - 预算标签：免费、低预算(50元内)、中等预算(50-200元)、高预算(200元以上)\n"
                "   - 时间标签：半日游(2-4小时)、一日游(4-8小时)、过夜游(需要住宿)\n"
                "4. 【数据要求】\n"
                "   - 优先推荐评分4.0以上、口碑好的景点\n"
                "   - 提供准确的门票价格和开放时间\n"
                "   - 简介要突出景点特色，不超过100字\n"
                "【JSON格式】\n"
                "{\"spotList\":[{\"name\":\"景点名\",\"latitude\":\"纬度\",\"longitude\":\"经度\",\"address\":\"地址\",\"score\":\"4.5分\",\"intro\":\"景点简介\",\"ticketPrice\":\"门票价格\",\"openTime\":\"开放时间\",\"type\":\"类型标签\"}]}"
            )
        )
        self.equip_tool(tool_manager.get_amap_tools())
