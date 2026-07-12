import logging
import os
from logging.handlers import RotatingFileHandler

_loggers = {}

def setup_logging(config):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    
    log_level = getattr(logging, config.logging.level.upper(), logging.INFO)
    max_bytes = config.logging.max_size_mb * 1024 * 1024
    backup_count = config.logging.backup_count
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    info_handler = RotatingFileHandler(
        f"{log_dir}/info.log", maxBytes=max_bytes, backupCount=backup_count
    )
    info_handler.setLevel(logging.INFO)
    info_handler.setFormatter(formatter)
    
    error_handler = RotatingFileHandler(
        f"{log_dir}/errors.log", maxBytes=max_bytes, backupCount=backup_count
    )
    error_handler.setLevel(logging.ERROR)
    error_handler.setFormatter(formatter)
    
    debug_handler = RotatingFileHandler(
        f"{log_dir}/debug.log", maxBytes=max_bytes, backupCount=backup_count
    )
    debug_handler.setLevel(logging.DEBUG)
    debug_handler.setFormatter(formatter)
    
    security_handler = RotatingFileHandler(
        f"{log_dir}/security.log", maxBytes=max_bytes, backupCount=backup_count
    )
    security_handler.setLevel(logging.INFO)
    security_handler.setFormatter(formatter)
    
    perf_handler = RotatingFileHandler(
        f"{log_dir}/performance.log", maxBytes=max_bytes, backupCount=backup_count
    )
    perf_handler.setLevel(logging.INFO)
    perf_handler.setFormatter(formatter)
    
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(info_handler)
    root_logger.addHandler(error_handler)
    root_logger.addHandler(debug_handler)
    
    _loggers["info"] = logging.getLogger("info")
    _loggers["error"] = logging.getLogger("error")
    _loggers["debug"] = logging.getLogger("debug")
    _loggers["security"] = logging.getLogger("security")
    _loggers["performance"] = logging.getLogger("performance")
    
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(formatter)
    root_logger.addHandler(console)
    
    logging.info("✅ Система логирования настроена")

def get_logger(name: str):
    return logging.getLogger(name)

def get_special_logger(name: str):
    return _loggers.get(name, logging.getLogger(name))
