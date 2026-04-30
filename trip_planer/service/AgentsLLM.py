import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List, Dict

from trip_planer.util.logger import logger

# 加载 .env 文件中的环境变量
load_dotenv(dotenv_path='D:\\pythonProject\\myAgent\\trip_planer\\env\\.env')

class AgentsLLM:
    """
    "Agents" 定制的LLM客户端。
    它用于调用任何兼容OpenAI接口的服务，并默认使用流式响应。
    """

    def __init__(self, model: str = None, apiKey: str = None, baseUrl: str = None, timeout: int = None):
        """
        初始化客户端。优先使用传入参数，如果未提供，则从环境变量加载。
        """
        self.model = model or os.getenv("LLM_MODEL_ID")
        apiKey = apiKey or os.getenv("LLM_API_KEY")
        baseUrl = baseUrl or os.getenv("LLM_BASE_URL")
        timeout = timeout or int(os.getenv("LLM_TIMEOUT", 300))


        if not all([self.model, apiKey, baseUrl]):
            raise ValueError("模型ID、API密钥和服务地址必须被提供或在.env文件中定义。")

        self.client = OpenAI(api_key=apiKey, base_url=baseUrl, timeout=timeout)

    def think_stream(self, messages: List[Dict[str, str]]):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=True
        )

        # 拿到大模型吐出的每一个碎片（chunk）
        for chunk in response:
            if not hasattr(chunk, 'choices') or len(chunk.choices) == 0:
                continue

            delta = chunk.choices[0].delta

            content = delta.content if (hasattr(delta, 'content') and delta.content is not None) else ""

            total_text = content

            if total_text:
                yield total_text

    def chat_with_tools(self, messages: List[Dict[str, str]], tools: List[Dict] = None, temperature: float = 0.1):
        """
        专门为 Agent 设计的方法，支持传入工具列表。
        为了精准解析模型返回的 JSON 函数参数，这里关闭流式输出。
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
        调用大语言模型进行思考，并在控制台流式打印，最后返回完整的响应字符串。
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

            for chunk in response:
                # 优化 1：更简洁地安全获取 choices 列表
                choices = getattr(chunk, 'choices', [])
                if not choices:
                    continue

                delta = choices[0].delta

                reasoning = getattr(delta, 'reasoning', None) or ""
                content = getattr(delta, 'content', None) or ""

                total_text = reasoning + content

                if total_text:
                    # 实时流式输出
                    print(total_text, end="", flush=True)
                    collected_content.append(total_text)

            print()  # 打印最后的换行
            full_result = "".join(collected_content)

            # 循环结束后，用 logger 统一记录一次完整的最终结果，存入日志文件
            logger.info(f"✅ [AgentsLLM] 思考完毕，完整回答长度: {len(full_result)} 字")

            return full_result

        except Exception as e:
            logger.info(f"❌ 大模型调用失败: {str(e)}")
            return f"思考出错：{str(e)}"

# --- 客户端使用示例 ---
if __name__ == '__main__':
    try:
        llmClient = AgentsLLM()

        exampleMessages = [
            {"role": "system", "content": "You are a helpful assistant that writes Python code."},
            {"role": "user", "content": "写一个快速排序算法"}
        ]

        print("--- 调用LLM ---")
        responseText = llmClient.think(exampleMessages)
        if responseText:
            print("\n\n--- 完整模型响应 ---")
            print(responseText)

    except ValueError as e:
        logger.info(e)
