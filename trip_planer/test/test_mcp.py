import asyncio
import sys
import os
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

# 加载 .env 里的高德 KEY
from dotenv import load_dotenv

load_dotenv(dotenv_path='../env/.env')


async def test_pure_mcp():
    print("1. 准备启动 MCP Server...")

    # 强制 Windows 使用 Proctor
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    # 关键修改：因为已经全局安装了，我们可以直接加 --no-install 甚至更换调用方式
    # 这样确保 npx 绝对保持安静，只输出 JSON
    cmd = "npx.cmd" if sys.platform == "win32" else "npx"
    server_params = StdioServerParameters(
        command=cmd,
        args=["--no-install", "@amap/amap-maps-mcp-server"],  # 强制不安装、不提示
        env={
            "AMAP_MAPS_API_KEY": os.getenv("GAODE_KEY", "你的高德key如果没配置请硬编码在这里测试"),
            "PATH": os.environ.get("PATH", "")
        }
    )

    try:
        print(f"2. 正在连接 stdio 管道... (命令: {cmd} {' '.join(server_params.args)})")
        # 建立底层管道
        async with stdio_client(server_params) as (read, write):
            print("3. 管道建立成功，正在初始化 MCP 协议握手...")
            # 建立会话
            async with ClientSession(read, write) as session:
                await session.initialize()
                print("4. 握手成功！正在获取工具列表...")

                tools_response = await session.list_tools()
                print(f"\n✅ 成功了！一共获取到 {len(tools_response.tools)} 个高德绝技：")
                for t in tools_response.tools:
                    print(f" 🎯 工具名: {t.name} -> 描述: {t.description[:30]}...")

    except Exception as e:
        print(f"\n❌ 彻底失败，捕获到极度底层的错误: {type(e).__name__} - {e}")


if __name__ == "__main__":
    asyncio.run(test_pure_mcp())