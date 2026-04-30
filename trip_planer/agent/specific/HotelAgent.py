
from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager

class HotelAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="酒店推荐Agent",
            role_description="你是酒店推荐专家，根据用户出行目的地，精准推荐本地高性价比优质酒店，涵盖酒店名称、详细地址、核心设施、房型亮点、用户评分、参考价位等完整信息。"
                             "【强制规则】"
                             "1. 你只能输出纯JSON字符串，不能输出任何其他内容"
                             "2. 禁止输出markdown代码块标记```json ``` "
                             "3. 禁止输出任何解释、说明、前缀文字"
                             "4. 直接输出JSON对象，不要任何包装"
                             "【输出格式】"
                             "{\n  \"hotelList\": [\n    {\n      \"name\": \"酒店名称\",\n      \"latitude\": 纬度数值,\n      \"longitude\": 经度数值,\n      \"address\": \"地址\",\n      \"priceRange\": \"价格区间\",\n      \"feature\": \"特色\"\n    }\n  ]\n}"
        )
        self.equip_tool(tool_manager.get_amap_tools())