from loguru import logger

logger.add("bot.log", rotation="10MB", retention="1 week", level="INFO", colorize=True, format="<green>{time:DD-MM-YYYY at HH:mm:ss}</green> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | <level>{level}</level> | {message}", enqueue=True, backtrace=True, diagnose=True)
