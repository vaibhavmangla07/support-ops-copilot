import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    """
    Returns a configured logger instance.
    - Console output
    - File output (rotating)
    """
    logger = logging.getLogger(name)
    
    # If the logger already has handlers, return it to avoid duplicate logs
    if logger.handlers:
        return logger
        
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File Handler (create logs dir if not exists)
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    file_handler = RotatingFileHandler(
        os.path.join(log_dir, "app.log"),
        maxBytes=5*1024*1024, # 5 MB
        backupCount=2
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger
