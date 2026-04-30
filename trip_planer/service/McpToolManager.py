# -*- coding: utf-8 -*-
"""
McpToolManager MCP 工具管理器模块

提供 MCP (Model Context Protocol) 工具的统一管理功能。
采用单例模式，确保全局只初始化一次工具。

主要功能：
- 工具注册：管理所有可用的 MCP 工具
- 工具获取：提供全局统一的工具获取接口
- 懒加载：工具在首次使用时才初始化，提高启动速度
- 单例模式：避免重复创建工具实例

使用示例：
    from trip_planer.service.McpToolManager import tool_manager
    
    # 获取高德地图工具
    amap_tools = tool_manager.get_amap_tools()
"""

import os
import sys
from dotenv import load_dotenv

from trip_planer.tools.MCPSubTool import MCPTool
from trip_planer.util.logger import logger

# 加载环境变量
load_dotenv(dotenv_path='/trip_planer/env/.env')


class McpToolManager:
    """
    MCP 工具管理器
    
    采用单例模式设计，全局只有一个工具管理器实例。
    负责管理和初始化各种 MCP 工具，如高德地图工具等。
    
    核心功能：
        - 工具注册：通过 get_amap_tools() 注册高德地图工具
        - 工具缓存：缓存已初始化的工具，避免重复创建
        - 环境变量：自动从 .env 文件读取 API 密钥
    
    属性说明：
        - amap_api_key: 高德地图 API 密钥
        - _amap_tool: 缓存的高德 MCP 工具实例
    """

    def __init__(self, gaode_key=None):
        """
        初始化工具管理器
        
        参数说明：
            gaode_key: 高德地图 API 密钥，默认从环境变量 GAODE_KEY 读取
        
        注意：
            - 使用单例模式，不要直接实例化此类
            - 请使用全局单例对象 tool_manager
        """
        self.amap_api_key = gaode_key or os.getenv("GAODE_KEY")
        self._amap_tool = None  # 工具实例缓存


    def get_amap_tools(self) -> MCPTool:
        """
        获取高德地图 MCP 工具
        
        这是获取高德地图工具的唯一入口。
        采用懒加载模式，首次调用时才会初始化工具。
        
        返回值：
            MCPTool: 高德地图 MCP 工具实例
        
        异常：
            ValueError: 如果未配置高德 API 密钥
        
        实现逻辑：
            1. 检查是否已缓存工具实例
            2. 如未缓存，检查 API 密钥是否配置
            3. 创建 MCPTool 实例（使用 npx 运行 @amap/amaps-mcp-server）
            4. 缓存并返回工具实例
        
        命令说明：
            - Windows: 使用 npx.cmd
            - Linux/Mac: 使用 npx
            - 参数 --no-install 屏蔽 npm install 干扰
        """
        # 检查是否已有缓存
        if self._amap_tool is None:
            # 验证 API 密钥
            if not self.amap_api_key:
                raise ValueError("请配置高德 KEY")

            logger.info("🚀 首次初始化高德 MCP 扩展坞...")

            # 兼容不同操作系统的命令
            # Windows 使用 npx.cmd，Linux/Mac 使用 npx
            cmd = "npx.cmd" if sys.platform == "win32" else "npx"

            # 创建 MCP 工具实例
            self._amap_tool = MCPTool(
                name="amap_mcp",
                command=cmd,
                # 加上 --no-install 屏蔽干扰
                args=["--no-install", "@amap/amap-maps-mcp-server"],
                env={"AMAP_MAPS_API_KEY": self.amap_api_key},
                auto_expand=True  # 自动展开子工具
            )
        
        return self._amap_tool


# 全局单例对象
# 使用此对象访问工具管理器，不要创建新的实例
tool_manager = McpToolManager()
