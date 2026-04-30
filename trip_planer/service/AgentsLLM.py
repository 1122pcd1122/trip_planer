# -*- coding: utf-8 -*-
"""
AgentsLLM 大语言模型客户端模块

提供与各种兼容 OpenAI API 的大语言模型服务交互的功能。
支持普通对话、工具调用、流式输出等多种模式。

主要功能：
- 普通对话：调用 LLM 进行文本生成
- 流式输出：实时获取 LLM 生成的每个 token
- 工具调用支持：支持 function calling 机制
- 环境配置：从 .env 文件加载 API 配置

配置说明（环境变量）：
    LLM_MODEL_ID: 模型 ID
    LLM_API_KEY: API 密钥
    LLM_BASE_URL: API 基础地址
    LLM_TIMEOUT: 请求超时时间（秒）
"""

import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

from trip_planer.util.logger import logger

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path='D:\\pythonProject\\myAgent\\trip_planer\\env\\.env')


class AgentsLLM:
    """
    大语言模型客户端
    
    封装 OpenAI SDK，提供统一的 LLM 调用接口。
    支持多种调用模式：
    - think(): 带流式输出的对话
    - think_stream(): 流式输出（逐字返回）
    - chat_with_tools(): 支持工具调用的对话
    
    初始化参数：
        - model: 模型 ID，默认从环境变量 LLM_MODEL_ID 读取
        - apiKey: API 密钥，默认从环境变量 LLM_API_KEY 读取
        - baseUrl: API 基础地址，默认从环境变量 LLM_BASE_URL 读取
        - timeout: 超时时间，默认从环境变量 LLM_TIMEOUT 读取（默认300秒）
    """

    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化 LLM 客户端
        
        参数说明：
            model: 模型标识符，如 "gpt-4"、"qwen-plus" 等
            apiKey: API 访问密钥
            baseUrl: API 服务的基础地址，如 "https://api.openai.com/v1"
            timeout: 请求超时时间（秒），默认 300 秒
        
        优先级：传入参数 > 环境变量
        
        异常：
            ValueError: 如果必要的配置项缺失
        """
        # 优先使用传入参数，否则从环境变量读取
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 300))

        # 验证必要参数
        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        # 初始化 OpenAI 客户端
        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)



    def chat_with_tools(self, messages: List[Dict[str, str]], tools: List[Dict] = None, temperature: float = 0.1) -> any:
        """
        支持工具调用的对话方法
        
        这是 Agent 系统的核心方法，用于实现 function calling 功能。
        LLM 可以根据对话内容决定是否调用外部工具，并返回工具调用信息。
        
        参数说明：
            messages: 对话历史列表
            tools: 工具定义列表，格式符合 OpenAI function calling 规范
            temperature: 生成温度，控制随机性，值越小越确定性越高
        
        返回值：
            message 对象，包含：
            - content: LLM 的文本回复
            - tool_calls: 工具调用列表（如果有）
        
        特点：
            - 关闭流式输出 (stream=False)，确保完整获取 tool_calls 对象
            - 支持 function calling 机制
            - 温度默认 0.1，保持较高确定性
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                tools=tools,
                stream=False  # 关闭流式，方便完整拿到 tool_calls 对象
            )
            # 直接返回官方的 message 对象，里面包含了 content 和 tool_calls
            return response.choices[0].message

        except Exception as e:
            logger.info(f"❌ Agent 推理出错: {str(e)}")
            return None


    def think(self, messages: List[Dict[str, str]], temperature: float = 0) -> str:
        """
        普通对话方法
        
        调用 LLM 进行文本生成，支持流式输出过程。
        
        参数说明：
            messages: 对话历史列表
            temperature: 生成温度，默认 0 表示最高确定性
        
        返回值：
            str: LLM 生成的完整文本内容
        
        执行流程：
            1. 调用 OpenAI API 创建流式响应
            2. 遍历每个 chunk，实时打印到控制台
            3. 收集所有内容并返回完整文本
            4. 记录日志
        
        注意：
            - 此方法不支持工具调用
            - 适用于需要流式展示但不需要工具调用的场景
        """
        logger.info(f"🧠 正在调用 {self.model} 模型...")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                stream=True,
            )

            logger.info("✅ 大语言模型响应成功:")
            collected_content = []

            # 遍历流式响应
            for chunk in response:
                # 优化：更简洁地安全获取 choices 列表
                choices = getattr(chunk, 'choices', [])
                if not choices:
                    continue

                delta = choices[0].delta

                # 安全获取 reasoning 和 content（支持推理模型）
                reasoning = getattr(delta, 'reasoning', None) or ""
                content = getattr(delta, 'content', None) or ""

                total_text = reasoning + content

                if total_text:
                    # 实时流式输出到控制台
                    print(total_text, end="", flush=True)
                    collected_content.append(total_text)

            print()  # 打印最后的换行
            full_result = "".join(collected_content)

            # 循环结束后，用 logger 统一记录一次完整的最终结果
            logger.info(f"✅ [AgentsLLM] 思考完毕，完整回答长度: {len(full_result)} 字")

            return full_result

        except Exception as e:
            logger.info(f"❌ 大模型调用失败: {str(e)}")
            return f"思考出错：{str(e)}"


# --- 客户端使用示例 ---
if __name__ == '__main__':
    """
    AgentsLLM 使用示例
    
    演示如何：
    1. 初始化客户端
    2. 构造消息列表
    3. 调用 think() 方法获取回复
    """
    try:
        llmClient = AgentsLLM()

        exampleMessages = [
            {"role": "system", "content": "You is a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]

        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        logger.info(e)
