import os
import sys
import json
from typing import List, Dict

from trip_planer.service.AgentsLLM import AgentsLLM
# 假设你在 service 目录下创建了我们上一轮讨论的管家
from trip_planer.service.McpToolManager import tool_manager
from trip_planer.util.logger import logger


class BaseAgent:
    """
    AgentsLLM 智能体基类 (支持工具调用版)
    """

    def __init__(self, name: str, role_description: str, llm_client: AgentsLLM = None):
        self.name = name
        self.llm = llm_client or AgentsLLM()

        # 1. 注入人设
        self.system_prompt = f"你是{name}。{role_description}"
        self.messages: List[Dict[str, str]] = [
            {"role": "system", "content": self.system_prompt}
        ]

        # 2. 工具箱：存放真实的工具实例和给大模型看的 Schema
        self.equipped_tools = {}  # 格式 { "工具名": 工具实例 }
        self.tools_schema = []  # 格式 [ {大模型认识的 JSON 说明书} ]


    def add_message(self, role: str, content: str):
        self.messages.append({"role": role, "content": content})


    def run_stream(self, prompt: str):
        self.add_message("user", prompt)

        full_reply = []  # 用于收集流式输出的完整内容，作为记忆保存

        # 直接透传底层大模型吐出来的每一个字
        for chunk in self.llm.think_stream(self.messages):
            full_reply.append(chunk)
            yield chunk  # 👈 拿到底层的一个字，继续往上层抛

        # 流式输出结束后，把完整的回答存入记忆，保证上下文不断档
        self.add_message("assistant", "".join(full_reply))

    def run(self, user_input: str) -> str:
        """
        带有工具调用的核心运行循环
        """
        print(f"\n[{self.name}] 收到任务: {user_input}")
        self.add_message("user", user_input)

        # -----------------------------------------------------
        # 阶段一：让模型思考 (评估是否需要使用已装配的工具)
        # -----------------------------------------------------
        tools_param = self.tools_schema if len(self.tools_schema) > 0 else None

        logger.info(f"🤖 [{self.name}] 正在思考对策 (评估是否需要使用工具)...")
        response_message = self.llm.chat_with_tools(
            messages=self.messages,
            tools=tools_param
        )

        if not response_message:
            return "思考失败，请检查网络或大模型服务。"

        # -----------------------------------------------------
        # 阶段二：解析模型意图，并在本地执行工具
        # -----------------------------------------------------
        if hasattr(response_message, 'tool_calls') and response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            logger.info(f"🛠️ [{self.name}] 决定使用工具: {function_name}，参数: {arguments}")

            # 记录模型的调用请求 (OpenAI 规范要求)
            self.messages.append(response_message)

            # 在本地找到对应的工具并执行
            if function_name in self.equipped_tools:
                target_tool = self.equipped_tools[function_name]

                # 假设 MCPTool 提供 execute 或 run 方法
                try:
                    tool_result = target_tool.execute(**arguments)
                    tool_result_str = str(tool_result)
                except Exception as e:
                    tool_result_str = f"工具执行失败: {str(e)}"

                # 将执行结果喂回给大模型
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
        """动态装配外部工具"""

        # 检查这是否是我们自己写的、带集合标记的 MCPTool
        if hasattr(tool, 'is_mcp_group') and tool.is_mcp_group:
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