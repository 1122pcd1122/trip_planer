# -*- coding: utf-8 -*-
"""
BaseAgent 基类模块

提供所有智能 Agent 的基础功能，包括：
- 大语言模型交互
- 工具调用机制
- 消息历史管理
- 工具动态装配

此类采用责任链模式设计，支持：
1. 普通对话模式：直接与 LLM 交互
2. 工具调用模式：自动评估并调用外部工具，获取结果后总结回答
"""


import json
from typing import List, Dict

from trip_planer.service.AgentsLLM import AgentsLLM
from trip_planer.service.McpToolManager import tool_manager
from trip_planer.util.logger import logger


class BaseAgent:
    """
    智能体基类
    
    所有专业 Agent（天气、景点、酒店、餐饮等）都继承自此类。
    此类封装了与 LLM 交互的核心逻辑，以及工具调用机制。
    
    核心功能：
        - system_prompt: 设置 Agent 角色人设
        - messages: 维护对话历史上下文
        - equipped_tools: 已装配的工具集合
        - tools_schema: 工具的 JSON Schema 描述
        - run(): 核心运行方法，支持自动工具调用
        - equip_tool(): 动态装配外部工具
    
    使用流程：
        1. 继承 BaseAgent 并设置 name 和 role_description
        2. 调用 equip_tool() 装配所需工具
        3. 调用 run() 方法执行任务
    """

    def __init__(self, name: str, role_description: str, llm_client: AgentsLLM = None):
        """
        初始化 Agent 实例
        
        参数说明：
            name: Agent 名称，用于日志输出和身份标识
            role_description: Agent 角色描述，定义其专业领域和行为方式
            llm_client: LLM 客户端实例，默认使用全局 AgentsLLM
        
        示例：
            weather_agent = WeatherAgent()
            等价于
            weather_agent = BaseAgent(name="天气助手", role_description="你是天气查询专家")
        """
        self.name = name
        self.llm = llm_client or AgentsLLM()

        # 1. 注入人设：构建 system prompt
        # System prompt 是 LLM 的系统指令，决定了 Agent 的行为风格和专业能力
        self.system_prompt = f"你是{name}。{role_description}"
        
        # 2. 消息历史：维护对话上下文
        # messages 列表存储所有对话记录，包括 system、user、assistant、tool 角色
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]

        # 3. 工具箱：存放真实的工具实例和给大模型看的 Schema
        # equipped_tools: 格式 { "工具名": 工具实例 }，用于执行工具
        # tools_schema: 格式 [ {大模型认识的 JSON 说明书} ]，用于告诉 LLM 可用工具
        self.equipped_tools = {}
        self.tools_schema = []


    def add_message(self, role: str, content: str):
        """
        向消息历史中添加一条消息
        
        参数说明：
            role: 消息角色，可选值 "system"、"user"、"assistant"、"tool"
            content: 消息内容
        
        示例：
            self.add_message("user", "今天天气怎么样？")
            self.add_message("assistant", "今天天气晴朗，气温25度。")
        """
        self.messages.append({"role": role, "content": content})


    def run(self, user_input: str) -> str:
        """
        带有工具调用的核心运行循环
        
        这是 Agent 的核心执行方法，处理完整的对话流程：
        1. 接收用户输入
        2. 让 LLM 评估是否需要使用工具
        3. 如需工具，执行工具并获取结果
        4. 将工具结果反馈给 LLM 生成最终回答
        
        参数说明：
            user_input: 用户输入的任务描述
        
        返回值：
            str: Agent 的最终回答内容
        
        执行流程：
            ┌─────────────────┐
            │  1. 用户输入     │
            └────────┬────────┘
                     ▼
            ┌─────────────────┐
            │  2. LLM 思考   │──── 不需要工具
            │  (评估工具)     │◄────────────┐
            └────────┬────────┘             │
                     ▼                     │
            ┌─────────────────┐           │
            │  3. 执行工具     │           │
            │  获取外部数据    │           │
            └────────┬────────┘             │
                     ▼                     │
            ┌─────────────────┐           │
            │  4. LLM 总结     │           │
            │  (生成最终回答)  │           │
            └────────┬────────┘           │
                     ▼                     │
            ┌─────────────────┐           │
            │  5. 返回结果    │───────────┘
            └─────────────────┘
        """
        logger.info(f"\n[{self.name}] 收到任务: {user_input}")
        self.add_message("user", user_input)

        # -----------------------------------------------------
        # 阶段一：让模型思考 (评估是否需要使用已装配的工具)
        # -----------------------------------------------------
        # 如果装配了工具，则传递给 LLM；否则设为 None
        tools_param = self.tools_schema if len(self.tools_schema) > 0 else None

        logger.info(f"🤖 [{self.name}] 正在思考对策 (评估是否需要使用工具)...")
        
        # 调用 LLM 的工具调用接口
        response_message = self.llm.chat_with_tools(
            messages=self.messages,
            tools=tools_param
        )

        if not response_message:
            return "思考失败，请检查网络或大模型服务。"

        # -----------------------------------------------------
        # 阶段二：解析模型意图，并在本地执行工具
        # -----------------------------------------------------
        # 检查 LLM 是否决定调用工具
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
            # 解析工具调用信息
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(f"🛠️ [{self.name}] 决定使用工具: {function_name}，参数: {arguments}")

            # 记录模型的调用请求 (OpenAI 规范要求)
            # 必须在 messages 中保留 tool_calls 信息
            self.messages.append(response_message)

            # 在本地找到对应的工具并执行
            if function_name in self.equipped_tools:
                target_tool = self.equipped_tools[function_name]

                # 执行工具调用
                try:
                    tool_result = target_tool.execute(**arguments)
                    tool_result_str = str(tool_result)
                except Exception as e:
                    tool_result_str = f"工具执行失败: {str(e)}"

                # 将执行结果喂回给大模型
                # role="tool" 表示这是工具返回的结果
                # tool_call_id 必须与之前的 tool_calls 匹配
                self.messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": tool_result_str
                })

                # -----------------------------------------------------
                # 阶段三：模型拿到工具结果后，总结为最终回答
                # -----------------------------------------------------
                logger.info(f"🧠 [{self.name}] 获取到外部数据，正在总结...")
                final_response = self.llm.think(self.messages)
                if final_response:
                    self.add_message("assistant", final_response)
                return final_response
            else:
                # 工具不存在的情况
                error_msg = f"未找到名为 {function_name} 的工具"
                logger.info(f"❌ {error_msg}")
                return error_msg

        else:
            # -----------------------------------------------------
            # 无需工具，直接回答
            # -----------------------------------------------------
            reply = response_message.content
            self.add_message("assistant", reply)
            logger.info(f"🗣️ [{self.name}] 直接回答: {reply}")
            return reply


    def equip_tool(self, tool):
        """
        动态装配外部工具
        
        支持两种工具格式：
        1. MCPTool (带 is_mcp_group 标记): 从扩展坞中解包所有子工具
        2. 普通工具: 直接装配
        
        参数说明：
            tool: 工具对象，可以是单个工具或工具组（扩展坞）
        
        装配流程：
            1. 检查工具是否为 MCP 扩展坞
            2. 如果是扩展坞，遍历解包所有子工具
            3. 将工具实例存入 equipped_tools
            4. 将工具 Schema 存入 tools_schema
        
        示例：
            # 装配单个工具
            self.equip_tool(weather_tool)
            
            # 装配工具组（扩展坞）
            amap_tool = tool_manager.get_amap_tools()
            self.equip_tool(amap_tool)
        """
        # 检查这是否是我们自己写的、带集合标记的 MCPTool
        if hasattr(tool, 'is_mcp_group') and tool.is_mcp_group:
            # 从扩展坞解包所有子工具并逐个装配
            for sub_tool in tool.get_sub_tools():
                self.equipped_tools[sub_tool.name] = sub_tool
                self.tools_schema.append(sub_tool.get_schema())
                logger.info(f"🔧 [{self.name}] 从扩展坞解包并装配技能: {sub_tool.name}")
        else:
            # 兼容普通单体工具的逻辑
            tool_schema = tool.get_schema()
            self.equipped_tools[tool.name] = tool
            self.tools_schema.append(tool_schema)
            logger.info(f"🔧 [{self.name}] 成功装配工具: {tool.name}")


# ==========================================
# 快速测试代码
# ==========================================
if __name__ == "__main__":
    """
    BaseAgent 基础功能测试
    
    此测试代码演示了如何：
    1. 创建一个基础 Agent
    2. 装配高德地图工具
    3. 执行带工具调用的任务
    """
    # 1. 实例化导游 Agent
    guide_agent = BaseAgent(
        name="金牌导游",
        role_description="你是一个专业的成都导游。你可以使用高德地图工具来查询天气和搜索景点。"
    )

    # 2. 获取并装配高德 MCP 扩展坞
    # 假设你在 McpToolManager.py 中实现了单例模式
    amap_tool = tool_manager.get_amap_tools()
    guide_agent.equip_tool(amap_tool)

    # 3. 运行测试
    print("=== 开始工具测试 ===")
    guide_agent.run("帮我查一下成都明天的天气怎么样？")
