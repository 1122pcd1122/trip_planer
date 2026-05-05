# -*- coding: utf-8 -*-
"""
AttractionAgent 景点推荐 Agent 模块

继承自 BaseAgent，专门负责景点推荐功能。
通过调用高德地图 API 获取目的地的热门景点信息。
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class AttractionAgent(BaseAgent):
    """景点推荐 Agent"""

    def __init__(self):
        super().__init__(
            name="景点推荐Agent",
            role_description=(
                "你是旅行策划师。根据用户输入的城市、天数和偏好标签，推荐景点并输出JSON。\n"
                "【规则】\n"
                "1. 直接输出纯JSON，禁止任何解释、markdown、前后缀\n"
                "2. 根据天数合理推荐数量：1-2天推荐3-5个，3-5天推荐6-10个\n"
                "3. 【关键】根据用户偏好标签精准匹配：\n"
                "   - 类型标签：自然风光、人文古迹、主题乐园、博物馆\n"
                "   - 场景标签：亲子游(适合儿童)、情侣约会(浪漫)、拍照打卡(网红)\n"
                "   - 强度标签：轻松休闲(步行即可)、体力挑战(登山/徒步)\n"
                "4. 优先推荐评分高、口碑好的景点\n"
                "【JSON格式】\n"
                "{\"spotList\":[{\"name\":\"景点名\",\"latitude\":\"\",\"longitude\":\"\",\"address\":\"地址\",\"score\":\"4.5分\",\"intro\":\"景点简介\"}]}"
            )
        )
        self.equip_tool(tool_manager.get_amap_tools())
