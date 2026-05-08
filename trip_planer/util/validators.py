# -*- coding: utf-8 -*-
"""
请求参数校验模块

提供统一的请求参数校验功能，使用 Pydantic 进行数据验证。
"""

from pydantic import BaseModel, ValidationError, field_validator
from typing import Optional
from trip_planer.util.date_utils import validate_date_format, validate_date_range


class PlanRequest(BaseModel):
    """旅行计划请求参数模型"""
    destination: str
    days: Optional[str] = "3"
    startDate: Optional[str] = ""
    endDate: Optional[str] = ""
    preferences: Optional[str] = ""
    
    @field_validator('destination')
    def destination_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('目的地不能为空')
        return v
    
    @field_validator('days')
    def days_valid(cls, v):
        if v and v.strip():
            try:
                days_int = int(v)
                if days_int < 1 or days_int > 30:
                    raise ValueError('游玩天数必须在1-30天之间')
            except ValueError:
                raise ValueError('游玩天数必须是数字')
        return v
    
    @field_validator('startDate')
    def start_date_valid(cls, v):
        if v and v.strip():
            if not validate_date_format(v):
                raise ValueError('开始日期格式错误，请使用 YYYY-MM-DD')
        return v
    
    @field_validator('endDate')
    def end_date_valid(cls, v):
        if v and v.strip():
            if not validate_date_format(v):
                raise ValueError('结束日期格式错误，请使用 YYYY-MM-DD')
        return v


class AuthRequest(BaseModel):
    """认证请求参数模型"""
    username: str
    password: str
    email: Optional[str] = ""
    
    @field_validator('username')
    def username_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('用户名不能为空')
        if len(v) < 3 or len(v) > 50:
            raise ValueError('用户名长度必须在3-50个字符之间')
        return v
    
    @field_validator('password')
    def password_valid(cls, v):
        if not v or v.strip() == "":
            raise ValueError('密码不能为空')
        if len(v) < 6:
            raise ValueError('密码长度至少6个字符')
        return v
    
    @field_validator('email')
    def email_valid(cls, v):
        if v and v.strip():
            if '@' not in v:
                raise ValueError('邮箱格式不正确')
        return v


class TripSaveRequest(BaseModel):
    """保存行程请求参数模型"""
    token: str
    trip_id: str
    destination: str
    days: int
    start_date: Optional[str] = ""
    end_date: Optional[str] = ""
    preferences: Optional[str] = ""
    trip_data: str
    
    @field_validator('token')
    def token_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Token 不能为空')
        return v
    
    @field_validator('trip_id')
    def trip_id_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('行程 ID 不能为空')
        return v
    
    @field_validator('destination')
    def destination_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('目的地不能为空')
        return v


class DetailRequest(BaseModel):
    """详情请求参数模型"""
    name: str
    latitude: Optional[str] = ""
    longitude: Optional[str] = ""
    
    @field_validator('name')
    def name_not_empty(cls, v):
        if not v or v.strip() == "":
            raise ValueError('名称不能为空')
        return v


def validate_request(model_cls, data):
    """
    统一参数校验函数
    
    参数：
        model_cls: Pydantic 模型类
        data: 请求数据（字典）
    
    返回：
        tuple: (校验后的数据, 错误信息)
    """
    try:
        validated = model_cls(**data)
        return validated.dict(), None
    except ValidationError as e:
        errors = []
        for error in e.errors():
            field = error.get('loc', ['unknown'])[0]
            msg = error.get('msg', '校验失败')
            errors.append(f"{field}: {msg}")
        return None, "; ".join(errors)