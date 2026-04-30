
from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager

class AttractionAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="景点推荐Agent",
            role_description=""
                             "你是景点推荐专家，根据用户目的地，精准推荐本地热门特色景点，包含景点名称、详细地址、核心看点、游玩亮点、开放时间、门票价格、游客评分、游玩时长等完整信息。"
                             "【强制规则】"
                             "1. 你只能输出纯JSON字符串，不能输出任何其他内容"
                             "2. 禁止输出markdown代码块标记```json ``` "
                             "3. 禁止输出任何解释、说明、前缀文字"
                             "4. 直接输出JSON对象，不要任何包装"
                             "【输出格式】"
                             "{\n  \"spotList\": [\n    {\n      \"name\": \"景点名称\",\n      \"latitude\": 纬度数值,\n      \"longitude\": 经度数值,\n      \"address\": \"地址\",\n      \"score\": \"评分\",\n      \"intro\": \"简介\"\n    }\n  ]\n}"
        )
        self.equip_tool(tool_manager.get_amap_tools())