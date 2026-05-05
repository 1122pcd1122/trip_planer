# -*- coding: utf-8 -*-
"""
用户认证服务

提供用户注册、登录、Token 验证等功能。
使用 SQLite 存储用户数据，JWT 进行身份验证。
"""

import sqlite3
import hashlib
import jwt
import os
from datetime import datetime, timedelta
from typing import Optional
from contextlib import contextmanager

from trip_planer.util.logger import logger


class AuthService:
    """用户认证服务"""
    
    SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "trip-planner-secret-key-change-in-production")
    TOKEN_EXPIRE_DAYS = 30
    
    def __init__(self, db_path: str = "users.db"):
        self.db_path = db_path
        self._init_db()
    
    def _get_connection(self):
        return sqlite3.connect(self.db_path)
    
    @contextmanager
    def get_db(self):
        conn = self._get_connection()
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()
    
    def _init_db(self):
        with self.get_db() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    email TEXT UNIQUE,
                    password_hash TEXT NOT NULL,
                    nickname TEXT,
                    avatar TEXT,
                    phone TEXT,
                    bio TEXT,
                    gender INTEGER DEFAULT 0,
                    birthday TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS user_trips (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    trip_id TEXT NOT NULL,
                    destination TEXT NOT NULL,
                    days INTEGER NOT NULL,
                    start_date TEXT,
                    end_date TEXT,
                    preferences TEXT,
                    trip_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    UNIQUE(user_id, trip_id)
                )
            """)
            logger.info("✅ 用户数据库初始化完成")
    
    def _hash_password(self, password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self, user_id: int, username: str) -> str:
        payload = {
            "user_id": user_id,
            "username": username,
            "exp": datetime.utcnow() + timedelta(days=self.TOKEN_EXPIRE_DAYS),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, self.SECRET_KEY, algorithm="HS256")
    
    def _verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None
    
    def register(self, username: str, password: str, email: str = "") -> dict:
        with self.get_db() as conn:
            existing = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
            if existing:
                return {"status": "error", "message": "用户名已存在", "code": "400"}
            
            if email:
                existing_email = conn.execute("SELECT id FROM users WHERE email = ?", (email,)).fetchone()
                if existing_email:
                    return {"status": "error", "message": "邮箱已被注册", "code": "400"}
            
            password_hash = self._hash_password(password)
            cursor = conn.execute(
                "INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)",
                (username, email, password_hash)
            )
            user_id = cursor.lastrowid
            token = self._generate_token(user_id, username)
            
            logger.info(f"✅ 用户注册成功: {username} (ID: {user_id})")
            return {
                "status": "success",
                "message": {
                    "user_id": user_id,
                    "username": username,
                    "token": token
                },
                "code": "200"
            }
    
    def login(self, username: str, password: str) -> dict:
        with self.get_db() as conn:
            user = conn.execute(
                "SELECT id, username, password_hash, nickname, email FROM users WHERE username = ?",
                (username,)
            ).fetchone()
            
            if not user:
                return {"status": "error", "message": "用户不存在", "code": "401"}
            
            if user["password_hash"] != self._hash_password(password):
                return {"status": "error", "message": "密码错误", "code": "401"}
            
            token = self._generate_token(user["id"], user["username"])
            
            conn.execute(
                "UPDATE users SET updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (user["id"],)
            )
            
            logger.info(f"✅ 用户登录成功: {username} (ID: {user['id']})")
            return {
                "status": "success",
                "message": {
                    "user_id": user["id"],
                    "username": user["username"],
                    "nickname": user["nickname"] or user["username"],
                    "email": user["email"],
                    "token": token
                },
                "code": "200"
            }
    
    def verify_token(self, token: str) -> dict:
        payload = self._verify_token(token)
        if not payload:
            return {"status": "error", "message": "Token 无效或已过期", "code": "401"}
        
        with self.get_db() as conn:
            user = conn.execute(
                "SELECT id, username, nickname, email, avatar, phone, bio, gender, birthday FROM users WHERE id = ?",
                (payload["user_id"],)
            ).fetchone()
            
            if not user:
                return {"status": "error", "message": "用户不存在", "code": "404"}
            
            return {
                "status": "success",
                "message": {
                    "user_id": user["id"],
                    "username": user["username"],
                    "nickname": user["nickname"] or user["username"],
                    "email": user["email"],
                    "avatar": user["avatar"],
                    "phone": user["phone"],
                    "bio": user["bio"],
                    "gender": user["gender"],
                    "birthday": user["birthday"]
                },
                "code": "200"
            }
    
    def save_trip(self, user_id: int, trip_id: str, destination: str, days: int,
                  start_date: str, end_date: str, preferences: str, trip_data: str) -> dict:
        with self.get_db() as conn:
            user = conn.execute("SELECT id FROM users WHERE id = ?", (user_id,)).fetchone()
            if not user:
                return {"status": "error", "message": "用户不存在", "code": "404"}
            
            conn.execute("""
                INSERT INTO user_trips (user_id, trip_id, destination, days, start_date, end_date, preferences, trip_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(user_id, trip_id) DO UPDATE SET
                    destination = excluded.destination,
                    days = excluded.days,
                    start_date = excluded.start_date,
                    end_date = excluded.end_date,
                    preferences = excluded.preferences,
                    trip_data = excluded.trip_data,
                    updated_at = CURRENT_TIMESTAMP
            """, (user_id, trip_id, destination, days, start_date, end_date, preferences, trip_data))
            
            logger.info(f"✅ 行程已保存: 用户 {user_id}, 行程 {trip_id}")
            return {"status": "success", "message": "行程已保存", "code": "200"}
    
    def get_trips(self, user_id: int) -> dict:
        with self.get_db() as conn:
            trips = conn.execute(
                "SELECT trip_id, destination, days, start_date, end_date, preferences, updated_at FROM user_trips WHERE user_id = ? ORDER BY updated_at DESC",
                (user_id,)
            ).fetchall()
            
            return {
                "status": "success",
                "message": [
                    {
                        "trip_id": row["trip_id"],
                        "destination": row["destination"],
                        "days": row["days"],
                        "start_date": row["start_date"],
                        "end_date": row["end_date"],
                        "preferences": row["preferences"],
                        "updated_at": row["updated_at"]
                    }
                    for row in trips
                ],
                "code": "200"
            }
    
    def get_trip(self, user_id: int, trip_id: str) -> dict:
        with self.get_db() as conn:
            trip = conn.execute(
                "SELECT trip_id, destination, days, start_date, end_date, preferences, trip_data, updated_at FROM user_trips WHERE user_id = ? AND trip_id = ?",
                (user_id, trip_id)
            ).fetchone()
            
            if not trip:
                return {"status": "error", "message": "行程不存在", "code": "404"}
            
            return {
                "status": "success",
                "message": {
                    "trip_id": trip["trip_id"],
                    "destination": trip["destination"],
                    "days": trip["days"],
                    "start_date": trip["start_date"],
                    "end_date": trip["end_date"],
                    "preferences": trip["preferences"],
                    "trip_data": trip["trip_data"],
                    "updated_at": trip["updated_at"]
                },
                "code": "200"
            }
    
    def delete_trip(self, user_id: int, trip_id: str) -> dict:
        with self.get_db() as conn:
            conn.execute(
                "DELETE FROM user_trips WHERE user_id = ? AND trip_id = ?",
                (user_id, trip_id)
            )
            logger.info(f"✅ 行程已删除: 用户 {user_id}, 行程 {trip_id}")
            return {"status": "success", "message": "行程已删除", "code": "200"}
