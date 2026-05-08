# -*- coding: utf-8 -*-
"""
日期工具函数模块

提供统一的日期处理功能，消除代码重复。
"""

from datetime import datetime, timedelta
from typing import Optional, Tuple


def format_date(date_obj: datetime) -> str:
    """将 datetime 对象格式化为字符串"""
    return date_obj.strftime("%Y-%m-%d")


def parse_date(date_str: str) -> Optional[datetime]:
    """解析日期字符串为 datetime 对象"""
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None


def calculate_days(start_date: str, end_date: str) -> Optional[int]:
    """根据开始日期和结束日期计算天数（包含首尾两天）"""
    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)
    
    if start_dt is None or end_dt is None:
        return None
    
    if end_dt < start_dt:
        return None
    
    return (end_dt - start_dt).days + 1


def calculate_end_date(start_date: str, days: int) -> Optional[str]:
    """根据开始日期和天数计算结束日期"""
    start_dt = parse_date(start_date)
    
    if start_dt is None:
        return None
    
    end_dt = start_dt + timedelta(days=days - 1)
    return format_date(end_dt)


def validate_date_format(date_str: str) -> bool:
    """验证日期格式是否为 YYYY-MM-DD"""
    return parse_date(date_str) is not None


def validate_date_range(start_date: str, end_date: str) -> bool:
    """验证日期范围是否有效（开始日期 <= 结束日期）"""
    start_dt = parse_date(start_date)
    end_dt = parse_date(end_date)
    
    if start_dt is None or end_dt is None:
        return False
    
    return start_dt <= end_dt


def get_today_str() -> str:
    """获取今天的日期字符串"""
    return format_date(datetime.now())


def get_date_range_from_days(start_date: str, days: int) -> Tuple[str, str]:
    """根据开始日期和天数获取日期范围"""
    end_date = calculate_end_date(start_date, days)
    return (start_date, end_date) if end_date else (start_date, start_date)