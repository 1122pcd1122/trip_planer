# -*- coding: utf-8 -*-
"""
全局异常处理模块

提供统一的异常处理和错误响应功能。
"""

from flask import jsonify
from trip_planer.util.logger import logger
import traceback


class ApiError(Exception):
    """自定义 API 错误异常"""
    
    def __init__(self, message: str, code: str = "500", status: str = "error"):
        self.message = message
        self.code = code
        self.status = status
        super().__init__(message)


class ValidationError(ApiError):
    """参数校验错误异常"""
    
    def __init__(self, message: str):
        super().__init__(message, code="400", status="error")


class AuthError(ApiError):
    """认证错误异常"""
    
    def __init__(self, message: str):
        super().__init__(message, code="401", status="error")


class NotFoundError(ApiError):
    """资源未找到错误异常"""
    
    def __init__(self, message: str):
        super().__init__(message, code="404", status="error")


class RateLimitError(ApiError):
    """限流错误异常"""
    
    def __init__(self, message: str = "请求过于频繁，请稍后再试"):
        super().__init__(message, code="429", status="error")


def make_error_response(error: ApiError):
    """创建统一的错误响应"""
    return jsonify({
        "status": error.status,
        "message": error.message,
        "code": error.code
    }), int(error.code)


def handle_generic_exception(e: Exception):
    """处理未捕获的异常"""
    logger.error(f"❌ 未捕获异常: {str(e)}")
    logger.error(f"   堆栈跟踪: {traceback.format_exc()}")
    
    return jsonify({
        "status": "error",
        "message": "服务器内部错误，请稍后重试",
        "code": "500"
    }), 500


def handle_api_error(e: ApiError):
    """处理自定义 API 错误"""
    logger.error(f"❌ API 错误: {e.code} - {e.message}")
    return make_error_response(e)


def handle_validation_error(e: ValidationError):
    """处理参数校验错误"""
    logger.warning(f"⚠️ 参数校验失败: {e.message}")
    return make_error_response(e)


def handle_auth_error(e: AuthError):
    """处理认证错误"""
    logger.warning(f"⚠️ 认证失败: {e.message}")
    return make_error_response(e)


def handle_not_found_error(e: NotFoundError):
    """处理资源未找到错误"""
    logger.warning(f"⚠️ 资源未找到: {e.message}")
    return make_error_response(e)


def handle_rate_limit_error(e: RateLimitError):
    """处理限流错误"""
    logger.warning(f"⚠️ 请求被限流: {e.message}")
    return make_error_response(e)


def register_exception_handlers(app):
    """注册全局异常处理器"""
    
    @app.errorhandler(Exception)
    def generic_exception_handler(e):
        return handle_generic_exception(e)
    
    @app.errorhandler(ApiError)
    def api_error_handler(e):
        return handle_api_error(e)
    
    @app.errorhandler(ValidationError)
    def validation_error_handler(e):
        return handle_validation_error(e)
    
    @app.errorhandler(AuthError)
    def auth_error_handler(e):
        return handle_auth_error(e)
    
    @app.errorhandler(NotFoundError)
    def not_found_error_handler(e):
        return handle_not_found_error(e)
    
    @app.errorhandler(RateLimitError)
    def rate_limit_error_handler(e):
        return handle_rate_limit_error(e)
    
    @app.errorhandler(404)
    def route_not_found_handler(e):
        return handle_not_found_error(NotFoundError("请求的资源不存在"))
    
    @app.errorhandler(400)
    def bad_request_handler(e):
        return handle_validation_error(ValidationError("请求参数错误"))
    
    logger.info("✅ 全局异常处理器已注册")