# -*- coding: utf-8 -*-
"""
WeatherService 和风天气服务模块

提供和风天气 API 的调用功能。
采用单例模式，全局共享 HTTP 会话，提高请求效率。

主要功能：
- 城市地理编码：通过城市名获取经纬度
- 天气预报查询：获取多天天气预报数据
- 天气数据处理：将 API 响应转换为标准格式

使用示例：
    from trip_planer.service.WeatherService import weather_service
    
    # 获取城市天气预报
    weather_data = weather_service.get_weather_forecast("成都", days=3)
"""

import os
import sys
import requests
from dotenv import load_dotenv
from trip_planer.util.logger import logger

# 加载环境变量
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', 'env', '.env'))


class WeatherService:
    """
    和风天气服务
    
    采用单例模式设计，全局共享一个实例。
    负责与和风天气 API 交互，获取天气预报数据。
    
    核心功能：
        - 城市地理编码查询
        - 多天天气预报获取
        - 数据格式转换
    
    属性说明：
        - api_key: 和风天气 API 密钥
        - base_url: API 基础 URL
        - geo_url: 地理编码 API URL
        - weather_url: 天气预报 API URL
    """

    def __init__(self, api_key=None):
        """
        初始化天气服务
        
        参数说明：
            api_key: 和风天气 API 密钥，默认从环境变量 QWEATHER_KEY 读取
        """
        self.api_key = api_key or os.getenv("QWEATHER_KEY")
        self.base_url = "https://devapi.qweather.com/v7"
        self.geo_url = "https://geoapi.qweather.com/v2"
        self.weather_url = f"{self.base_url}/weather/3d"
        logger.info(f'Weather Service 和风天气 API Key: {self.api_key[:8]}***' if self.api_key else 'Weather Service 未配置 API Key')

    def get_city_location(self, city_name: str) -> dict:
        """
        通过城市名获取经纬度（地理编码）
        
        参数说明：
            city_name: 城市名称，例如 "成都"
        
        返回值：
            dict: 包含 location_id, latitude, longitude 的字典
            如果查询失败，返回空字典
        
        注意：
            - 使用和风天气的 GeoAPI
            - 默认查询中国城市，如需查询国外城市需修改 range 参数
        """
        if not self.api_key:
            logger.error("❌ 未配置和风天气 API Key")
            return {}

        try:
            url = f"{self.geo_url}/city/lookup"
            params = {
                "location": city_name,
                "key": self.api_key,
                "range": "cn",  # 仅查询中国城市
                "number": 1     # 只返回最匹配的结果
            }

            logger.info(f"🌍 正在查询城市 [{city_name}] 的地理信息...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != "200" or not data.get("location"):
                logger.warning(f"⚠️ 未找到城市 [{city_name}] 的地理信息")
                return {}

            location = data["location"][0]
            result = {
                "location_id": location["id"],
                "city_name": location["name"],
                "latitude": location["lat"],
                "longitude": location["lon"]
            }

            logger.info(f"✅ 城市 [{city_name}] 地理信息查询成功: {result}")
            return result

        except requests.exceptions.Timeout:
            logger.error("❌ 地理编码请求超时")
            return {}
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 地理编码请求失败: {str(e)}")
            return {}
        except Exception as e:
            logger.error(f"❌ 地理编码处理失败: {str(e)}")
            return {}

    def get_weather_forecast(self, city_name: str, days: int = 3) -> dict:
        """
        获取城市多天天气预报
        
        参数说明：
            city_name: 城市名称，例如 "成都"
            days: 需要查询的天数，最多 3 天
        
        返回值：
            dict: 标准格式的天气数据，包含 weatherList 列表
            如果查询失败，返回包含错误信息的字典
        
        标准格式：
            {
                "weatherList": [
                    {
                        "cityName": "成都",
                        "latitude": "30.57",
                        "longitude": "104.07",
                        "date": "2024-01-01",
                        "weather": "多云转晴",
                        "temperature": "8~15℃",
                        "tips": "天气适宜出行，建议携带薄外套"
                    }
                ]
            }
        """
        if not self.api_key:
            logger.error("❌ 未配置和风天气 API Key")
            return {"error": "未配置和风天气 API Key"}

        # 先获取城市地理编码
        location = self.get_city_location(city_name)
        if not location:
            return {"error": f"无法找到城市 [{city_name}] 的信息"}

        try:
            url = self.weather_url
            params = {
                "location": location["location_id"],
                "key": self.api_key
            }

            logger.info(f"🌤️ 正在查询 [{city_name}] 的天气预报 (days={days})...")
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("code") != "200" or not data.get("daily"):
                logger.warning(f"⚠️ 未获取到 [{city_name}] 的天气数据")
                return {"error": f"无法获取 [{city_name}] 的天气数据"}

            # 解析天气数据
            daily_forecasts = data["daily"][:min(days, 3)]  # 最多取 3 天
            weather_list = []

            for day in daily_forecasts:
                # 生成天气提示
                tips = self._generate_weather_tips(day)

                weather_item = {
                    "cityName": location["city_name"],
                    "latitude": location["latitude"],
                    "longitude": location["longitude"],
                    "date": day["fxDate"],
                    "weather": f"{day['textDay']}转{day['textNight']}",
                    "temperature": f"{day['tempMin']}~{day['tempMax']}℃",
                    "tips": tips
                }
                weather_list.append(weather_item)

            result = {"weatherList": weather_list}
            logger.info(f"✅ [{city_name}] 天气预报查询成功，返回 {len(weather_list)} 天数据")
            return result

        except requests.exceptions.Timeout:
            logger.error("❌ 天气预报请求超时")
            return {"error": "天气查询超时，请稍后重试"}
        except requests.exceptions.RequestException as e:
            logger.error(f"❌ 天气预报请求失败: {str(e)}")
            return {"error": f"天气查询失败: {str(e)}"}
        except Exception as e:
            logger.error(f"❌ 天气数据处理失败: {str(e)}")
            return {"error": f"天气数据处理失败: {str(e)}"}

    def _generate_weather_tips(self, weather_data: dict) -> str:
        temp_min = self._parse_temp(weather_data.get("tempMin", "0"))
        temp_max = self._parse_temp(weather_data.get("tempMax", "0"))
        weather_day = weather_data.get("textDay", "")
        weather_night = weather_data.get("textNight", "")
        wind_dir = weather_data.get("windDirDay", "")
        wind_scale = weather_data.get("windScaleDay", "")

        tips_parts = []

        if temp_max >= 35:
            tips_parts.append("天气炎热，注意防晒和补水")
        elif temp_max >= 28:
            tips_parts.append("天气较热，建议穿轻便透气的衣物")
        elif temp_min >= 20 and temp_max <= 28:
            tips_parts.append("温度适宜，适合户外活动")
        elif temp_min >= 10:
            tips_parts.append("天气微凉，建议携带薄外套")
        elif temp_min >= 0:
            tips_parts.append("天气较冷，注意保暖")
        else:
            tips_parts.append("天气寒冷，建议穿厚衣服并戴手套")

        if "雨" in weather_day or "雨" in weather_night:
            tips_parts.append("有降雨，记得携带雨伞")
        if "雪" in weather_day or "雪" in weather_night:
            tips_parts.append("有降雪，注意防滑")
        if "雾" in weather_day or "雾" in weather_night:
            tips_parts.append("有雾，出行注意安全")
        if "霾" in weather_day or "霾" in weather_night:
            tips_parts.append("空气质量较差，建议佩戴口罩")

        if wind_scale:
            wind_val = self._parse_temp(wind_scale)
            if wind_val >= 5:
                tips_parts.append(f"风力较大（{wind_dir} {wind_scale}级），注意防风")

        return "，".join(tips_parts) + "。"

    def _parse_temp(self, value: str) -> int:
        if not value:
            return 0
        value = str(value).replace("℃", "").strip()
        if "-" in value:
            parts = value.split("-")
            try:
                nums = [int(p.strip()) for p in parts if p.strip().lstrip("-").isdigit()]
                return sum(nums) // len(nums) if nums else 0
            except ValueError:
                return 0
        try:
            return int(value)
        except ValueError:
            return 0


# 全局单例对象
# 使用此对象访问天气服务，不要创建新的实例
weather_service = WeatherService()
