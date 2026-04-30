# trip_planer/utils/logger.py
import logging
import os
from logging.handlers import RotatingFileHandler

# 1. 自动创建 logs 文件夹
log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "logs")
os.makedirs(log_dir, exist_ok=True)

# 2. 初始化全局 Logger
logger = logging.getLogger("SmartTravel")
logger.setLevel(logging.DEBUG) # 捕捉所有级别的日志

# 3. 定义极其清晰的结构化日志格式
# 格式：[时间] [级别] [文件名:行号] - 具体信息
formatter = logging.Formatter(
    fmt="[%(asctime)s] [%(levelname)s] [%(filename)s:%(lineno)d] - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# 防止重复添加 Handler
if not logger.handlers:
    # 4. 控制台输出 (方便开发时实时看)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO) # 控制台只看 INFO 及以上
    console_handler.setFormatter(formatter)

    # 5. 文件输出 (核心：保存到文件，随时可看)
    # RotatingFileHandler 可以限制文件大小，比如 5MB 满后自动创建新文件备份
    log_file_path = os.path.join(log_dir, "agent_system.log")
    file_handler = RotatingFileHandler(
        filename=log_file_path,
        maxBytes=5 * 1024 * 1024, # 5MB
        backupCount=3,            # 保留3个备份
        encoding="utf-8"          # 必须用 utf-8，否则控制台的 Emoji 和中文会乱码
    )
    file_handler.setLevel(logging.DEBUG) # 文件里保存最全的日志，包括 DEBUG
    file_handler.setFormatter(formatter)

    # 装配 Handler
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)