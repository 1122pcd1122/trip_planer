
from trip_planer.agent.base.BaseAgent import BaseAgent
from trip_planer.service.McpToolManager import tool_manager


class RestaurantAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="美食推荐Agent",
            role_description="你是餐饮推荐专家，根据用户目的地推荐本地特色美食，包括餐厅名称、地址、招牌菜、评分等信息。"
                             "【强制规则】"
                             "1. 你只能输出纯JSON字符串，不能输出任何其他内容"
                             "2. 禁止输出markdown代码块标记```json ``` "
                             "3. 禁止输出任何解释、说明、前缀文字"
                             "4. 直接输出JSON对象，不要任何包装"
                             "【输出格式】"
                             "{  \"foodList\": [\n    {\n      \"name\": \"店铺名称\",\n      \"latitude\": 纬度数值,\n      \"longitude\": 经度数值,\n      \"address\": \"地址\",\n      \"featureDish\": \"招牌菜\",\n      \"score\": \"评分\"\n    }\n  ]\n}"
        )
        self.equip_tool(tool_manager.get_amap_tools())