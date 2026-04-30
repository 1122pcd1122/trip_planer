# -*- coding: utf-8 -*-
"""
MCPSubTool MCP 工具封装模块

提供 MCP (Model Context Protocol) 工具的封装实现。
将外部 MCP 服务（如高德地图）封装为统一的工具接口。

主要包含两个类：
- MCPTool: MCP 工具扩展坞，负责启动和管理 MCP 服务进程
- MCPSubTool: 从扩展坞中解包出的独立技能，供 Agent 使用

工作原理：
    1. MCPTool 启动子进程运行 MCP Server（如 @amap/amap-maps-mcp-server）
    2. 通过 stdio 与子进程通信
    3. 获取可用的工具列表
    4. 将每个工具封装为 MCPSubTool 供 Agent 调用

使用示例：
    from trip_planer.tools.MCPSubTool import MCPTool
    
    # 创建 MCP 工具
    tool = MCPTool(
        name="amap_mcp",
        command="npx",
        args=["--no-install", "@amap/amap-maps-mcp-server"],
        env={"AMAP_MAPS_API_KEY": "your_key"}
    )
    
    # 获取子工具列表
    sub_tools = tool.get_sub_tools()
"""

import os
import asyncio
import sys
import threading
from mcp import ClientSession, StdioServerParameters, stdio_client

from trip_planer.util.logger import logger


class MCPSubTool:
    """
    MCP 子工具类
    
    从 MCP 扩展坞中解包出来的独立技能。
    封装了单个工具的名称、描述、参数等信息。
    
    属性说明：
        - name: 工具名称
        - description: 工具功能描述
        - parameters: 工具参数 Schema
        - _session_manager: 会话管理器，用于执行工具调用
    
    主要方法：
        - get_schema(): 生成给大模型看的标准工具说明书
        - execute(): 真正调用 MCP Server 执行工具
    """

    def __init__(self, name, description, parameters, session_manager):
        """
        初始化子工具
        
        参数说明：
            name: 工具名称，如 "weather"、maps_search_place"
            description: 工具功能描述，供 LLM 理解工具用途
            parameters: 工具输入参数的定义，JSON Schema 格式
            session_manager: 会话管理器，用于实际执行工具调用
        """
        self.name = name
        self.description = description
        self.parameters = parameters
        self._session_manager = session_manager


    def get_schema(self):
        """
        生成给大模型看的标准工具说明书
        
        将工具信息转换为 OpenAI Function Calling 格式的 Schema。
        LLM 通过此 Schema 理解工具的用途和参数。
        
        返回值：
            dict: 符合 OpenAI function calling 规范的工具定义
        
        示例：
            {
                "type": "function",
                "function": {
                    "name": "weather",
                    "description": "查询城市天气",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "city": {"type": "string", "description": "城市名称"}
                        },
                        "required": ["city"]
                    }
                }
            }
        """
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters
            }
        }


    def execute(self, **kwargs):
        """
        真正调用 MCP Server 去执行工具
        
        通过会话管理器发送工具调用请求到 MCP Server。
        
        参数说明：
            **kwargs: 工具所需的参数，键值对形式
        
        返回值：
            str: 工具执行结果
        
        示例：
            tool.execute(city="成都", date="2024-01-01")
        """
        return self._session_manager.call_tool_sync(self.name, kwargs)


class MCPTool:
    """
    MCP 工具扩展坞类
    
    负责启动和管理 MCP 服务进程，提供统一的工具接口。
    支持自动解包子工具，供 Agent 直接使用。
    
    核心功能：
        - 进程管理：启动/维护 MCP Server 子进程
        - 通信管理：通过 stdio 与子进程双向通信
        - 工具解包：自动获取并封装可用工具为 MCPSubTool
        - 跨平台支持：自动处理 Windows/Linux/Mac 差异
    
    属性说明：
        - name: 扩展坞名称
        - command: 启动命令（如 npx、python 等）
        - args: 命令参数列表
        - env: 环境变量字典
        - is_mcp_group: 标记为工具组，供 BaseAgent 识别
        - _sub_tools: 解包后的子工具列表
    """

    def __init__(self, name: str, command: str, args: list, env: dict = None, auto_expand: bool = True):
        """
        初始化 MCP 工具扩展坞
        
        参数说明：
            name: 扩展坞名称
            command: 启动命令，如 "npx"、"python" 等
            args: 命令参数列表，如 ["--no-install", "@amap/amap-maps-mcp-server"]
            env: 环境变量字典，可选
            auto_expand: 是否自动解包子工具，默认 True
        
        实现细节：
            - 自动处理 Windows 下的 npx.cmd 问题
            - 创建后台事件循环处理异步通信
            - 启动子进程并建立 stdio 连接
            - 获取可用工具列表并封装
        """
        self.name = name

        # 🔧 修复 1: 自动处理 Windows 下的 npx 后缀问题
        if sys.platform == 'win32' and command == 'npx':
            self.command = 'npx.cmd'
        else:
            self.command = command

        self.args = args

        # 设置环境变量
        self.env = os.environ.copy()
        if env:
            self.env.update(env)

        # 标记为工具组，供 BaseAgent 识别并自动解包
        self.is_mcp_group = auto_expand
        self._sub_tools = []

        # Windows 下设置事件循环策略（解决 asyncio 兼容问题）
        if sys.platform == 'win32':
            asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

        # 创建后台事件循环和线程
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._run_loop, daemon=True)
        self._thread.start()

        # 初始化连接并获取工具列表
        self._init_sync()


    def _run_loop(self):
        """
        运行后台事件循环
        
        在独立线程中运行 asyncio 事件循环，
        用于处理与 MCP Server 的异步通信。
        """
        asyncio.set_event_loop(self._loop)
        self._loop.run_forever()


    def _run_coroutine_sync(self, coro):
        """
        将异步方法转为同步阻塞等待
        
        由于 MCP 通信是异步的，但 Agent 调用是同步的，
        此方法用于在同步上下文中调用异步方法。
        
        参数说明：
            coro: 协程对象
        
        返回值：
            协程的返回值
        
        超时：
            60秒，超时则抛出异常
        """
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        return future.result(timeout=60)


    async def _async_init(self):
        """
        异步的初始化与连接过程
        
        执行以下操作：
        1. 创建 Server 参数
        2. 建立 stdio 客户端连接
        3. 创建 ClientSession
        4. 初始化会话
        5. 获取可用工具列表并封装
        """
        # 创建 Server 参数
        server_params = StdioServerParameters(
            command=self.command,
            args=self.args,
            env=self.env
        )
        
        # 创建 stdio 客户端
        self._cm = stdio_client(server_params)
        self._read, self._write = await self._cm.__aenter__()

        # 👇 核心修复区：手动激活 ClientSession 的监听循环
        self._session_cm = ClientSession(self._read, self._write)
        self.session = await self._session_cm.__aenter__()
        await self.session.initialize()

        # 获取可用工具列表
        tools_response = await self.session.list_tools()
        for t in tools_response.tools:
            # 将它们封装成 Agent 能听懂的 SubTool
            self._sub_tools.append(MCPSubTool(
                name=t.name,
                description=t.description,
                parameters=t.inputSchema,
                session_manager=self
            ))


    def _init_sync(self):
        """
        同步初始化方法
        
        包装异步初始化过程，提供同步调用接口。
        在日志中输出初始化状态。
        """
        logger.info(f"🔄 正在启动 MCP 扩展坞: {self.command} {' '.join(self.args)}")
        self._run_coroutine_sync(self._async_init())
        logger.info(f"✅ 扩展坞连接成功！自动展开了 {len(self._sub_tools)} 个底层工具。")


    def get_sub_tools(self) -> list:
        """
        获取解包后的子工具列表
        
        返回值：
            list: MCPSubTool 实例列表
        
        使用场景：
            BaseAgent 调用 equip_tool() 时使用
        """
        return self._sub_tools


    async def _async_call_tool(self, tool_name, arguments):
        """
        异步发送指令给 MCP Server 执行
        
        参数说明：
            tool_name: 工具名称
            arguments: 工具参数字典
        
        返回值：
            str: 工具执行结果文本
        """
        result = await self.session.call_tool(tool_name, arguments)
        if result.content:
            return result.content[0].text
        return "执行成功，无返回内容"


    def call_tool_sync(self, tool_name, arguments):
        """
        暴露给 Agent 的同步执行接口
        
        Agent 通过此方法调用实际的 MCP 工具。
        
        参数说明：
            tool_name: 要调用的工具名称
            arguments: 工具参数字典
        
        返回值：
            str: 工具执行结果
        
        异常处理：
            捕获所有异常并返回错误信息字符串
        """
        logger.info(f"▶️ [底层] 发送网络请求执行 MCP: {tool_name}")
        try:
            return self._run_coroutine_sync(self._async_call_tool(tool_name, arguments))
        except Exception as e:
            return f"MCP调用失败: {str(e)}"
