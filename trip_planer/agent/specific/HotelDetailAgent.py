# -*- coding: utf-8 -*-
"""
HotelDetailAgent 酒店详情 Agent 模块

继承自 BaseAgent，专门负责获取单个酒店的详细信息。
通过调用高德地图 API 获取酒店的详细数据。

主要功能：
- 酒店详情查询：获取特定酒店的完整信息
- 信息完善：提供酒店设施、房型、评分、联系方式等详细信息
- 地理位置：返回酒店的经纬度坐标

输出格式：纯 JSON 字符串，包含酒店详情的各个字段
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class HotelDetailAgent(BaseAgent):
    """
    酒店详情 Agent
    
    继承自 BaseAgent，专门用于获取单个酒店的详细信息。
    装配高德地图工具，通过调用外部 API 获取酒店详情数据。
    
    核心职责：
        - 接收酒店名称和坐标
        - 调用高德地图酒店详情查询 API
        - 解析返回的酒店详细数据
        - 生成符合规范的 JSON 格式输出
    
    输出 JSON 字段说明：
        - name: 酒店名称
        - address: 酒店地址
        - phone: 联系电话
        - rating: 评分（如"4.8分"）
        - priceRange: 价格区间
        - feature: 酒店特色/亮点
        - facilities: 设施列表
        - roomTypes: 房型介绍
        - checkInTime: 入住时间
        - checkOutTime: 退房时间
        - description: 酒店简介
    """

    def __init__(self):
        """
        初始化酒店详情 Agent
        
        设置 Agent 名称和角色描述，同时装配高德地图工具。
        
        角色描述要点：
            - 专业定位：酒店详情查询专家
            - 查询内容：单个酒店的完整详细信息
        
        输出规范（强制规则）：
            1. 仅输出纯 JSON 字符串，不包含任何其他内容
            2. 禁止输出 markdown 代码块标记
            3. 禁止输出任何解释、说明、前缀文字
            4. 直接输出 JSON 对象，不需要任何包装
        """
        super().__init__(
            name="酒店详情Agent",
            role_description=""
                             "你是专业酒店详情查询专家，专门获取单个酒店的完整详细信息。"
                             "用户输入酒店名称和坐标后，你必须："
                             "1. 使用高德地图API查询该酒店的详细信息"
                             "2. 整理并输出完整的酒店详情JSON"
                             ""
                             "【核心任务】"
                             "- 接收酒店名称+坐标 → 调用酒店详情查询工具 → 直接输出JSON"
                             "- 【禁止】不要进行任何额外搜索或调用其他工具"
                             ""
                             "【强制输出规则】"
                             "1. 直接输出JSON，不要有任何思考过程、解释文字"
                             "2. 仅输出纯JSON字符串，禁止任何解释、前缀、后缀"
                             "3. 禁止使用markdown代码块标记"
                             "4. JSON必须包含以下字段：name, address, phone, rating, priceRange, feature, facilities, roomTypes, checkInTime, checkOutTime, description"
                             ""
                             "【输出JSON格式】"
                             "{\"name\":\"酒店名称\",\"address\":\"酒店地址\",\"phone\":\"联系电话\",\"rating\":\"评分\",\"priceRange\":\"价格区间\",\"feature\":\"酒店特色\",\"facilities\":\"设施列表\",\"roomTypes\":\"房型介绍\",\"checkInTime\":\"入住时间\",\"checkOutTime\":\"退房时间\",\"description\":\"酒店简介\"}"
        )
        # 装配高德地图工具，获取酒店详情查询能力
        self.equip_tool(tool_manager.get_amap_tools())
