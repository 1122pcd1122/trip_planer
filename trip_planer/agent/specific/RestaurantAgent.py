# -*- coding: utf-8 -*-
"""
RestaurantAgent 餐饮推荐 Agent 模块

继承自 BaseAgent，专门负责餐饮推荐功能。
通过调用高德地图 API 获取目的地的特色美食餐厅信息。
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class RestaurantAgent(BaseAgent):
    """餐饮推荐 Agent"""

    def __init__(self):
        super().__init__(
            name="美食推荐Agent",
            role_description=(
                "你是美食侦探。根据用户输入的城市、天数和偏好标签，推荐餐厅并输出JSON。\n"
                "【规则】\n"
                "1. 直接输出纯JSON，禁止任何解释、markdown、前后缀\n"
                "2. 根据天数合理推荐数量：每天2-3家，涵盖午晚两餐\n"
                "3. 【关键】根据用户偏好标签精准匹配：\n"
                "   - 菜系标签：川菜、粤菜、湘菜、日料、韩餐、西餐\n"
                "   - 类型标签：火锅、烧烤、小吃、快餐、甜品、自助餐\n"
                "   - 偏好标签：不吃辣(推荐清淡菜系)、素食(推荐素食餐厅)、清真\n"
                "   - 场景标签：网红店、老字号、路边摊、大排档\n"
                "4. 优先推荐评分高、口碑好的本地特色餐厅\n"
                "【JSON格式】\n"
                "{\"foodList\":[{\"name\":\"餐厅名\",\"latitude\":\"\",\"longitude\":\"\",\"address\":\"地址\",\"featureDish\":\"招牌菜\",\"score\":\"4.5分\"}]}"
            )
        )
        self.equip_tool(tool_manager.get_amap_tools())
