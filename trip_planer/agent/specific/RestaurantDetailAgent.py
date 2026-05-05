# -*- coding: utf-8 -*-
"""
RestaurantDetailAgent 餐厅详情 Agent 模块

继承自 BaseAgent，专门负责获取单个餐厅的详细信息。
通过调用高德地图 API 获取餐厅的详细数据。

主要功能：
- 餐厅详情查询：获取特定餐厅的完整信息
- 信息完善：提供餐厅招牌菜、营业时间、人均消费、联系方式等详细信息
- 地理位置：返回餐厅的经纬度坐标

输出格式：纯 JSON 字符串，包含餐厅详情的各个字段
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class RestaurantDetailAgent(BaseAgent):
    """
    餐厅详情 Agent
    
    继承自 BaseAgent，专门用于获取单个餐厅的详细信息。
    装配高德地图工具，通过调用外部 API 获取餐厅详情数据。
    
    核心职责：
        - 接收餐厅名称和坐标
        - 调用高德地图餐厅详情查询 API
        - 解析返回的餐厅详细数据
        - 生成符合规范的 JSON 格式输出
    
    输出 JSON 字段说明：
        - name: 餐厅名称
        - address: 餐厅地址
        - phone: 联系电话
        - rating: 评分（如"4.6分"）
        - avgPrice: 人均消费
        - openTime: 营业时间
        - featureDish: 招牌菜/特色菜
        - description: 餐厅简介
        - cuisineType: 菜系类型
        - seats: 座位数/环境描述
    """

    def __init__(self):
        """
        初始化餐厅详情 Agent
        
        设置 Agent 名称和角色描述，同时装配高德地图工具。
        
        角色描述要点：
            - 专业定位：餐厅详情查询专家
            - 查询内容：单个餐厅的完整详细信息
        
        输出规范（强制规则）：
            1. 仅输出纯 JSON 字符串，不包含任何其他内容
            2. 禁止输出 markdown 代码块标记
            3. 禁止输出任何解释、说明、前缀文字
            4. 直接输出 JSON 对象，不需要任何包装
        """
        super().__init__(
            name="餐厅详情Agent",
            role_description=""
                             "你是专业餐厅详情查询专家，专门获取单个餐厅的完整详细信息。"
                             "用户输入餐厅名称和坐标后，你必须："
                             "1. 使用高德地图API查询该餐厅的详细信息"
                             "2. 整理并输出完整的餐厅详情JSON"
                             ""
                             "【核心任务】"
                             "- 接收餐厅名称+坐标 → 调用餐厅详情查询工具 → 直接输出JSON"
                             "- 【禁止】不要进行任何额外搜索或调用其他工具"
                             ""
                             "【强制输出规则】"
                             "1. 直接输出JSON，不要有任何思考过程、解释文字"
                             "2. 仅输出纯JSON字符串，禁止任何解释、前缀、后缀"
                             "3. 禁止使用markdown代码块标记"
                             "4. JSON必须包含以下字段：name, address, phone, rating, avgPrice, openTime, featureDish, description, cuisineType, seats"
                             ""
                             "【输出JSON格式】"
                             "{\"name\":\"餐厅名称\",\"address\":\"餐厅地址\",\"phone\":\"联系电话\",\"rating\":\"评分\",\"avgPrice\":\"人均消费\",\"openTime\":\"营业时间\",\"featureDish\":\"招牌菜\",\"description\":\"餐厅简介\",\"cuisineType\":\"菜系类型\",\"seats\":\"座位数/环境描述\"}"
        )
        # 装配高德地图工具，获取餐厅详情查询能力
        self.equip_tool(tool_manager.get_amap_tools())
