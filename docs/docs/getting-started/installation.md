# 安装部署

本指南介绍如何安装和部署智能旅行助手 API 服务。

## 环境要求

- Python 3.8+
- pip 包管理器
- 有效的 LLM API 密钥

## 安装步骤

### 1. 克隆项目

```bash
git clone https://github.com/trip-planner/Android.git
cd Android/Agent
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置环境变量

创建 `.env` 文件并配置以下变量：

```bash
# LLM API 配置
LLM_API_KEY=your_api_key_here
LLM_BASE_URL=https://api.example.com/v1
LLM_MODEL=gpt-4

# 高德地图 API 配置
AMAP_API_KEY=your_amap_key_here
```

### 4. 启动服务

```bash
python -m trip_planer.main_api
```

服务将在 `http://localhost:8000` 启动。

## 验证安装

运行健康检查：

```bash
curl http://localhost:8000/
```

预期响应：

```json
{
  "status": "ok",
  "message": "Welcome to Smart Travel Assistant API!",
  "code": "200"
}
```

## 生产部署

### 使用 Gunicorn

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8000 "trip_planer.main_api:app"
```

### 使用 Docker

```dockerfile
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["python", "-m", "trip_planer.main_api"]
```

构建和运行：

```bash
docker build -t trip-planner-api .
docker run -p 8000:8000 trip-planner-api
```

## 常见问题

### Q: 启动时提示模块未找到

确保在项目根目录下运行：

```bash
cd Agent
python -m trip_planer.main_api
```

### Q: LLM API 连接失败

检查 `.env` 文件中的 API 配置是否正确。

### Q: 高德地图 API 返回错误

确认 API 密钥有效且有足够的调用额度。
