# -*- coding: utf-8 -*-
"""
RestaurantAgent 餐饮推荐 Agent 模块

继承自 BaseAgent，专门负责餐饮推荐功能。
通过调用高德地图 API 获取目的地的特色美食餐厅信息。

主要功能：
- 餐饮查询：获取城市内的特色美食餐厅
- 信息完善：提供餐厅名称、地址、招牌菜、评分等完整信息
- 地理位置：返回餐厅的经纬度坐标，便于地图展示

输出格式：纯 JSON 字符串，包含 foodList 数组，每个元素包含 name、latitude、longitude、address、featureDish、score 等字段
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class RestaurantAgent(BaseAgent):
    """
    餐饮推荐 Agent
    
    继承自 BaseAgent，专门用于处理餐饮推荐请求。
    装配高德地图工具，通过调用外部 API 获取餐厅数据。
    
    核心职责：
        - 接收餐饮推荐请求
        - 调用高德地图餐饮 POI 搜索 API
        - 解析返回的餐厅数据
        - 生成符合规范的 JSON 格式输出
    
    输出 JSON 字段说明：
        - foodList: 餐厅列表数组
          - name: 餐厅名称
          - latitude: 餐厅纬度
          - longitude: 餐厅经度
          - address: 餐厅地址
          - featureDish: 招牌菜/特色美食（如"麻辣火锅"、"小龙虾"、"烤鸭"等）
          - score: 顾客评分（如"4.5分"、"4.8分"等）
    """

    def __init__(self):
        """
        初始化餐饮推荐 Agent
        
        设置 Agent 名称和角色描述，同时装配高德地图工具。
        
        角色描述要点：
            - 专业定位：餐饮推荐专家
            - 查询内容：本地特色美食、餐厅名称、地址、招牌菜、评分
        
        输出规范（强制规则）：
            1. 仅输出纯 JSON 字符串，不包含任何其他内容
            2. 禁止输出 markdown 代码块标记（如 ```json ```）
            3. 禁止输出任何解释、说明、前缀文字
            4. 直接输出 JSON 对象，不需要任何包装
        """
        super().__init__(
            name="美食推荐Agent",
            role_description=""
                             "你是专业美食侦探，精通各地美食与餐厅筛选。用户输入目的地城市、游玩天数和偏好后，你必须："
                             "1. 使用高德地图API搜索该城市特色餐厅（类型：中餐、火锅、小吃、烧烤、日料、西餐等）"
                             "2. 根据游玩天数合理推荐餐厅数量（建议：每天2-3家，涵盖午晚两餐）"
                             ""
                             "【核心任务】"
                             "- 接收城市+天数+偏好 → 调用餐饮搜索工具 → 直接输出JSON"
                             "- 【禁止】不要进行任何额外搜索或调用其他工具"
                             ""
                             "【强制输出规则】"
                             "1. 直接输出JSON，不要有任何思考过程、解释文字"
                             "2. 仅输出纯JSON字符串，禁止任何解释、前缀、后缀"
                             "3. 禁止使用markdown代码块标记"
                             "4. JSON必须包含foodList数组，每个元素包含：name, latitude, longitude, address, featureDish, score（如无经纬度则为空字符串）"
                             ""
                             "【输出JSON格式】"
                             "{\"foodList\":[{\"name\":\"餐厅名\",\"latitude\":\"\",\"longitude\":\"\",\"address\":\"地址\",\"featureDish\":\"招牌菜\",\"score\":\"评分\"}]}"
        )
        # 装配高德地图工具，获取餐饮搜索能力
        self.equip_tool(tool_manager.get_amap_tools())
