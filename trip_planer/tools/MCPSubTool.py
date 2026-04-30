import os
import asyncio
import sys
import threading
from mcp import ClientSession, StdioServerParameters, stdio_client

from trip_planer.util.logger import logger


class MCPSubTool:
    """内部类：从 MCP 扩展坞中自动“解包”出来的独立技能"""

    def __init__(self, name, description, parameters, session_manager):
        self.name = name
        self.description = description
        self.parameters = parameters
        self._session_manager = session_manager

    def get_schema(self):
        """生成给大模型看的标准说明书"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }

    def execute(self, **kwargs):
        """真正调用 MCP Server 去执行"""
        return self._session_manager.call_tool_sync(self.name, kwargs)


class MCPTool:
    """
    你专属的 MCP 工具扩展坞实现！
    负责启动子进程、维系通信、并解析可用工具。
    """

    def __init__(self, name: str, command: str, args: list, env: dict = None, auto_expand: bool = True):
        self.name = name

        # 🔧 修复 1: 自动处理 Windows 下的 npx 后缀问题
        if sys.platform == 'win32' and command == 'npx':
            self.command = 'npx.cmd'
        else:
            self.command = command

        self.args = args

        self.env = os.environ.copy()
        if env:
            self.env.update(env)

        self.is_mcp_group = auto_expand
        self._sub_tools = []

        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

        # 初始化连接并获取工具列表
        self._init_sync()

    def _run_loop(self):
        """运行后台事件循环"""
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()

    def _run_coroutine_sync(self, coro):
        """将异步方法强制转为同步阻塞等待"""
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout=60)

    async def _async_init(self):
        """异步的初始化与连接过程"""
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.env
        )
        self._cm = stdio_client(server_params)
        self._read, self._write = await self._cm.__aenter__()

        # 👇 核心修复区：手动激活 ClientSession 的监听循环
        self._session_cm = ClientSession(self._read, self._write)
        self.session = await self._session_cm.__aenter__()
        await self.session.initialize()

        tools_response = await self.session.list_tools()
        for t in tools_response.tools:
            # 将它们封装成你的 Agent 能听懂的 SubTool
            self._sub_tools.append(MCPSubTool(
                name=t.name,
                description=t.description,
                parameters=t.inputSchema,
                session_manager=self
            ))

    def _init_sync(self):
        logger.info(f"🔄 正在启动 MCP 扩展坞: {self.command} {' '.join(self.args)}")
        self._run_coroutine_sync(self._async_init())
        logger.info(f"✅ 扩展坞连接成功！自动展开了 {len(self._sub_tools)} 个底层工具。")

    def get_sub_tools(self) -> list:
        return self._sub_tools

    async def _async_call_tool(self, tool_name, arguments):
        """异步发送指令给 Node.js 进程执行"""
        result = await self.session.call_tool(tool_name, arguments)
        if result.content:
            return result.content[0].text
        return "执行成功，无返回内容"

    def call_tool_sync(self, tool_name, arguments):
        """暴露给 Agent 的同步执行接口"""
        logger.info(f"▶️ [底层] 发送网络请求执行 MCP: {tool_name}")
        try:
            return self._run_coroutine_sync(self._async_call_tool(tool_name, arguments))
        except Exception as e:
            return f"MCP调用失败: {str(e)}"