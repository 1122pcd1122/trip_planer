"""
MCP 工具连接测试模块

本模块用于测试与高德地图 MCP Server 的直接连接
验证 MCP 协议是否能正常初始化并获取可用工具列表

用途：
- 调试 MCP 连接问题
- 验证高德 API Key 配置是否正确
- 确认 MCP Server 提供的工具可用性

前置条件：
1. 全局安装 Node.js 和 npx
2. 配置高德地图 API Key（AMAP_MAPS_API_KEY）
3. MCP Server 包已安装：npm install -g @amap/amap-maps-mcp-server

使用说明：
python -m trip_planer.test.test_mcp
"""

import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 加载 .env 里的高德 KEY
from dotenv import load_dotenv

load_dotenv(dotenv_path='../env/.env')


async def test_pure_mcp():
    """
    测试 MCP Server 连接的主函数

    执行流程：
    1. 配置 Windows 事件循环策略（解决 Windows 兼容性问题）
    2. 构建 MCP Server 启动参数
    3. 建立 stdio 管道连接
    4. 初始化 MCP 协议会话
    5. 获取并列出可用工具

    异常处理：
    - 捕获连接错误、协议握手失败、工具获取失败等情况
    - 提供详细的错误信息帮助定位问题

    注意：
    - Windows 系统使用 npx.cmd，Linux/Mac 使用 npx
    - --no-install 参数避免重复安装提示
    """
    print("1. 准备启动 MCP Server...")

    # 强制 Windows 使用 Proctor 事件循环
    # Windows 原生 asyncio 在某些场景下有兼容性问题
    # WindowsProactorEventLoopPolicy 提供更好的性能和支持
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # 构建 MCP Server 启动命令参数
    # cmd: 根据操作系统选择 npx 命令（Windows: npx.cmd, Unix: npx）
    # args: MCP Server 包名，--no-install 避免重复安装
    # env: 传递高德地图 API Key 到 Server 进程
    cmd = "npx.cmd" if sys.platform == "win32" else "npx"
    server_params = StdioServerParameters(
        command=cmd,
        args=["--no-install", "@amap/amap-maps-mcp-server"],
        env={
            "AMAP_MAPS_API_KEY": os.getenv("GAODE_KEY", "你的高德key如果没配置请硬编码在这里测试"),
            "PATH": os.environ.get("PATH", "")
        }
    )

    try:
        print(f"2. 正在连接 stdio 管道... (命令: {cmd} {' '.join(server_params.args)})")
        # 建立底层管道（stdio: 标准输入输出）
        # MCP Server 作为子进程运行，通过 stdin/stdout 与客户端通信
        async with stdio_client(server_params) as (read, write):
            print("3. 管道建立成功，正在初始化 MCP 协议握手...")
            # 建立 MCP 会话并初始化协议
            # 这一步会交换协议版本、协商能力等
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("4. 握手成功！正在获取工具列表...")

                # 调用 list_tools 获取 MCP Server 提供的能力列表
                tools_response = await session.list_tools()
                print(f"\n✅ 成功了！一共获取到 {len(tools_response.tools)} 个高德绝技：")
                for t in tools_response.tools:
                    # 打印每个工具的名称和描述（截取前30字符）
                    print(f" 🎯 工具名: {t.name} -> 描述: {t.description[:30]}...")

    except Exception as e:
        # 捕获所有底层错误并打印详细信息
        # 常见错误：API Key 无效、权限不足、网络问题、版本不兼容等
        print(f"\n❌ 彻底失败，捕获到极度底层的错误: {type(e).__name__} - {e}")


if __name__ == "__main__":
    """
    模块入口

    使用 asyncio.run() 启动异步测试函数
    这是 Python 3.7+ 推荐的异步编程入口方式
    """
    asyncio.run(test_pure_mcp())
