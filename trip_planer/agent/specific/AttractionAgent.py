# -*- coding: utf-8 -*-
"""
AttractionAgent 景点推荐 Agent 模块

继承自 BaseAgent，专门负责景点推荐功能。
通过调用高德地图 API 获取目的地的热门景点信息。

主要功能：
- 景点查询：获取城市内的热门旅游景点
- 信息完善：提供景点名称、地址、评分、简介等完整信息
- 地理位置：返回景点的经纬度坐标，便于地图展示和路线规划

输出格式：纯 JSON 字符串，包含 spotList 数组，每个元素包含 name、latitude、longitude、address、score、intro 等字段
"""

from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class AttractionAgent(BaseAgent):
    """
    景点推荐 Agent
    
    继承自 BaseAgent，专门用于处理景点推荐请求。
    装配高德地图工具，通过调用外部 API 获取景点数据。
    
    核心职责：
        - 接收景点推荐请求
        - 调用高德地图 POI 搜索 API
        - 解析返回的景点数据
        - 生成符合规范的 JSON 格式输出
    
    输出 JSON 字段说明：
        - spotList: 景点列表数组
          - name: 景点名称
          - latitude: 景点纬度
          - longitude: 景点经度
          - address: 景点地址
          - score: 游客评分（如"4.5分"、"4.8分"等）
          - intro: 景点简介/特色介绍
    """

    def __init__(self):
        """
        初始化景点推荐 Agent
        
        设置 Agent 名称和角色描述，同时装配高德地图工具。
        
        角色描述要点：
            - 专业定位：景点推荐专家
            - 查询内容：热门特色景点、景点详情（地址、看点、亮点、开放时间、门票、评分、游玩时长）
        
        输出规范（强制规则）：
            1. 仅输出纯 JSON 字符串，不包含任何其他内容
            2. 禁止输出 markdown 代码块标记（如 ```json ```）
            3. 禁止输出任何解释、说明、前缀文字
            4. 直接输出 JSON 对象，不需要任何包装
        """
        super().__init__(
            name="景点推荐Agent",
            role_description=""
                             "你是专业旅行策划师，精通景点规划与特色发现。用户输入目的地城市、游玩天数和偏好后，你必须："
                             "1. 使用高德地图API搜索该城市热门景点（类型：风景名胜、休闲娱乐、人文古迹等）"
                             "2. 根据游玩天数合理规划推荐数量（建议：1-2天推荐3-5个，3-5天推荐6-10个）"
                             ""
                             "【核心任务】"
                             "- 接收城市+天数+偏好 → 调用POI搜索工具 → 直接输出JSON"
                             "- 【禁止】不要进行任何额外搜索或调用其他工具"
                             ""
                             "【强制输出规则】"
                             "1. 直接输出JSON，不要有任何思考过程、解释文字"
                             "2. 仅输出纯JSON字符串，禁止任何解释、前缀、后缀"
                             "3. 禁止使用markdown代码块标记"
                             "4. JSON必须包含spotList数组，每个元素包含：name, latitude, longitude, address, score, intro（如无经纬度则为空字符串）"
                             ""
                             "【输出JSON格式】"
                             "{\"spotList\":[{\"name\":\"景点名\",\"latitude\":\"\",\"longitude\":\"\",\"address\":\"地址\",\"score\":\"评分\",\"intro\":\"简介\"}]}"
        )
        # 装配高德地图工具，获取景点搜索能力
        self.equip_tool(tool_manager.get_amap_tools())
