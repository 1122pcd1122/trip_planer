import os
import sys

from trip_planer.agent.CoordinatorAgent import CoordinatorAgent

# 1. 解决目录引入问题 (确保能找到 trip_planer 包)
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from trip_planer.service.McpToolManager import tool_manager


def main():
    print("===========================================")
    print("🚀 启动智能旅行助手 (MCP 动态装配版) 测试...")
    print("===========================================\n")

    # 2. 实例化智能体大脑
    guide_agent = CoordinatorAgent()

    # 3. 获取并装配 MCP 扩展坞
    try:
        print("⏳ 正在请求加载全局高德 MCP 扩展坞...")
        # 这里会触发 npx 后台进程的启动
        amap_tools = tool_manager.get_amap_tools()

        # 将扩展坞交给 Agent，Agent 内部会触发自动解包 (auto_expand)
        guide_agent.equip_tool(amap_tools)

    except Exception as e:
        print(f"\n❌ 工具加载失败！请检查:\n1. .env 文件中是否配置了 GAODE_KEY\n2. 电脑是否安装了 Node.js\n错误详情: {e.args}")
        return

    print("\n✅ 核心引擎准备完毕！开始模拟真实用户对话...\n")
    print("-" * 50)

    # ==========================================
    # 测试用例 1：天气查询 (测试参数提取和工具执行)
    # ==========================================
    question_1 = "我打算明天去成都玩，帮我查一下成都市的天气怎么样？出门需要带伞吗？"
    guide_agent.run(question_1)

    print("-" * 50)

    print("🎉 自动化测试脚本执行完毕！")


if __name__ == "__main__":
    main()