import os
import sys
from dotenv import load_dotenv

from trip_planer.tools.MCPSubTool import MCPTool
from trip_planer.util.logger import logger

load_dotenv(dotenv_path='/trip_planer/env/.env')  # 确保路径对


class McpToolManager:
    """全局工具注册中心"""

    def __init__(self, gaode_key=None):
        self.amap_api_key = gaode_key or os.getenv("GAODE_KEY")
        self._amap_tool = None

    def get_amap_tools(self) -> MCPTool:
        if self._amap_tool is None:
            if not self.amap_api_key:
                raise ValueError("请配置高德 KEY")

            logger.info("🚀 首次初始化高德 MCP 扩展坞...")

            # 兼容 Windows 的命令后缀
            cmd = "npx.cmd" if sys.platform == "win32" else "npx"

            self._amap_tool = MCPTool(
                name="amap_mcp",
                command=cmd,
                # 加上我们测试成功的 --no-install 屏蔽干扰
                args=["--no-install", "@amap/amap-maps-mcp-server"],
                env={"AMAP_MAPS_API_KEY": self.amap_api_key},
                auto_expand=True
            )
        return self._amap_tool


tool_manager = McpToolManager()