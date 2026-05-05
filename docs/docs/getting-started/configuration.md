# 配置说明

本指南介绍智能旅行助手 API 的各项配置选项。

## 配置文件

### 环境变量 (.env)

```bash
# LLM 配置
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=gpt-4

# 高德地图 API
AMAP_API_KEY=your_amap_key_here

# 服务配置
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### 配置项说明

| 配置项 | 说明 | 默认值 | 必填 |
|--------|------|--------|------|
| LLM_API_KEY | LLM API 密钥 | - | ✅ |
| LLM_BASE_URL | LLM API 地址 | - | ✅ |
| LLM_MODEL | 使用的模型名称 | gpt-4 | ❌ |
| AMAP_API_KEY | 高德地图 API 密钥 | - | ✅ |
| HOST | 服务监听地址 | 0.0.0.0 | ❌ |
| PORT | 服务端口 | 8000 | ❌ |
| DEBUG | 调试模式 | true | ❌ |

## Agent 配置

每个 Agent 都有独立的角色描述和工具配置，可在 `agent/specific/` 目录下的文件中修改。

### 修改 Agent 角色

```python
# 在 HotelAgent.py 中
super().__init__(
    name="酒店推荐Agent",
    role_description="你是专业酒店顾问..."  # 修改此处
)
```

## 日志配置

日志配置在 `util/logger.py` 中：

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### 日志级别

- DEBUG: 调试信息
- INFO: 一般信息
- WARNING: 警告信息
- ERROR: 错误信息
- CRITICAL: 严重错误
