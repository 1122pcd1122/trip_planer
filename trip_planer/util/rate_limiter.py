# -*- coding: utf-8 -*-
"""
请求限流工具模块

提供统一的限流配置和管理功能，使用 Flask-Limiter 实现。
"""

from flask import Flask, request
from trip_planer.util.logger import logger
from trip_planer.util.exception_handler import RateLimitError


try:
    from flask_limiter import Limiter
    from flask_limiter.util import get_remote_address
    HAS_LIMITER = True
except ImportError:
    Limiter = None
    get_remote_address = None
    HAS_LIMITER = False


limiter = None


def init_limiter(app: Flask):
    """
    初始化限流器

    参数：
        app: Flask 应用实例
    """
    global limiter

    if not HAS_LIMITER:
        logger.warning("⚠️ flask-limiter 未安装，限流功能已禁用")
        return

    limiter = Limiter(
        key_func=get_remote_address,
        app=app,
        default_limits=["200 per minute", "10 per second"],
        storage_uri="memory://",
        strategy="fixed-window"
    )

    @app.errorhandler(RateLimitError)
    def handle_rate_limit_error(e):
        return {
            "status": "error",
            "message": str(e),
            "code": "429"
        }, 429

    logger.info("✅ 限流器初始化完成")


def get_limiter():
    """获取限流器实例"""
    return limiter


def rate_limit(limit_string: str, key_func=None):
    """
    限流装饰器

    参数：
        limit_string: 限流规则，如 "10 per minute"
        key_func: 限流键函数，默认为客户端 IP
    """
    if limiter is None:
        return lambda f: f

    return limiter.limit(limit_string, key_func=key_func)


API_RATE_LIMITS = {
    "/api/plan": "20 per minute",
    "/api/weather": "30 per minute",
    "/api/attraction": "30 per minute",
    "/api/hotel": "30 per minute",
    "/api/restaurant": "30 per minute",
    "/api/hotel/detail": "50 per minute",
    "/api/attraction/detail": "50 per minute",
    "/api/restaurant/detail": "50 per minute",
    "/api/auth/register": "5 per minute",
    "/api/auth/login": "10 per minute",
    "/api/trip/save": "20 per minute",
    "/api/trip/list": "30 per minute",
    "/api/trip/get": "50 per minute",
    "/api/trip/delete": "20 per minute",
}


def apply_api_rate_limits():
    """为所有 API 路由应用限流规则"""
    pass