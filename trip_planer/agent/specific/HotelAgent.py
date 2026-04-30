# -*- coding: utf-8 -*-
"""
HotelAgent 酒店推荐 Agent 模块

继承自 BaseAgent，专门负责酒店推荐功能。
通过调用高德地图 API 获取目的地的优质酒店信息。

主要功能：
- 酒店查询：获取城市内的优质酒店
- 信息完善：提供酒店名称、地址、设施、房型、价格等完整信息
- 地理位置：返回酒店的经纬度坐标，便于地图展示

输出格式：纯 JSON 字符串，包含 hotelList 数组，每个元素包含 name、latitude、longitude、address、priceRange、feature 等字段
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class HotelAgent(BaseAgent):
    """
    酒店推荐 Agent
    
    继承自 BaseAgent，专门用于处理酒店推荐请求。
    装配高德地图工具，通过调用外部 API 获取酒店数据。
    
    核心职责：
        - 接收酒店推荐请求
        - 调用高德地图酒店 POI 搜索 API
        - 解析返回的酒店数据
        - 生成符合规范的 JSON 格式输出
    
    输出 JSON 字段说明：
        - hotelList: 酒店列表数组
          - name: 酒店名称
          - latitude: 酒店纬度
          - longitude: 酒店经度
          - address: 酒店地址
          - priceRange: 价格区间（如"300-500元"、"500-800元"等）
          - feature: 酒店特色/房型亮点（如"海景房"、"近地铁"、"亲子酒店"等）
    """

    def __init__(self):
        """
        初始化酒店推荐 Agent
        
        设置 Agent 名称和角色描述，同时装配高德地图工具。
        
        角色描述要点：
            - 专业定位：酒店推荐专家
            - 查询内容：高性价比优质酒店、地址、设施、房型、评分、价格
        
        输出规范（强制规则）：
            1. 仅输出纯 JSON 字符串，不包含任何其他内容
            2. 禁止输出 markdown 代码块标记（如 ```json ```）
            3. 禁止输出任何解释、说明、前缀文字
            4. 直接输出 JSON 对象，不需要任何包装
        """
        super().__init__(
            name="酒店推荐Agent",
            role_description=""
                             "你是专业酒店顾问，精通酒店筛选与预订建议。用户输入目的地城市、游玩天数和偏好后，你必须："
                             "1. 使用高德地图API搜索该城市优质酒店（类型：豪华型、舒适型、经济型、民宿等）"
                             "2. 根据游玩天数合理推荐酒店数量（建议：短途1-2家，中长途3-5家）"
                             ""
                             "【核心任务】"
                             "- 接收城市+天数+偏好 → 调用酒店搜索工具 → 直接输出JSON"
                             "- 【禁止】不要进行任何额外搜索或调用其他工具"
                             ""
                             "【强制输出规则】"
                             "1. 直接输出JSON，不要有任何思考过程、解释文字"
                             "2. 仅输出纯JSON字符串，禁止任何解释、前缀、后缀"
                             "3. 禁止使用markdown代码块标记"
                             "4. JSON必须包含hotelList数组，每个元素包含：name, latitude, longitude, address, priceRange, feature（如无经纬度则为空字符串）"
                             ""
                             "【输出JSON格式】"
                             "{\"hotelList\":[{\"name\":\"酒店名\",\"latitude\":\"\",\"longitude\":\"\",\"address\":\"地址\",\"priceRange\":\"价格区间\",\"feature\":\"特色\"}]}"
        )
        # 装配高德地图工具，获取酒店搜索能力
        self.equip_tool(tool_manager.get_amap_tools())
