# -*- coding: utf-8 -*-
"""
HotelAgent 酒店推荐 Agent 模块

继承自 BaseAgent，专门负责酒店推荐功能。
通过调用高德地图 API 获取目的地的优质酒店信息。
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class HotelAgent(BaseAgent):
    """酒店推荐 Agent"""

    def __init__(self):
        super().__init__(
            name="酒店推荐Agent",
            role_description=(
                "你是酒店顾问。根据用户输入的城市、天数和偏好标签，推荐酒店并输出JSON。\n"
                "【规则】\n"
                "1. 直接输出纯JSON，禁止任何解释、markdown、前后缀\n"
                "2. 根据天数合理推荐数量：短途1-2家，中长途3-5家\n"
                "3. 【关键】根据用户偏好标签精准匹配：\n"
                "   - 档次标签：经济型(100-300元)、舒适型(300-500元)、高档型(500-800元)、豪华型(800元以上)\n"
                "   - 特色标签：亲子酒店(近乐园/有儿童设施)、情侣酒店(浪漫氛围)、商务酒店(近CBD)\n"
                "   - 设施标签：含早餐、近地铁(500米内)、停车场、游泳池\n"
                "4. 优先推荐评分高、性价比高的酒店\n"
                "【JSON格式】\n"
                "{\"hotelList\":[{\"name\":\"酒店名\",\"latitude\":\"\",\"longitude\":\"\",\"address\":\"地址\",\"priceRange\":\"300-500元\",\"feature\":\"特色标签\"}]}"
            )
        )
        self.equip_tool(tool_manager.get_amap_tools())
