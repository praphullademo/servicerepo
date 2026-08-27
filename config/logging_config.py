"""
Logging configuration module for environment-based logging levels.
- DEBUG level for non-production environments
- ERROR level for production environments
"""

import logging
import os
from logging.handlers import RotatingFileHandler


def get_environment():
    """
    Detect current environment.
    
    Returns:
        str: Environment name (PROD, STAGING, DEVELOPMENT, etc.)
    """
    return os.getenv('ENVIRONMENT', 'DEVELOPMENT').upper()


def get_log_level():
    """
    Determine log level based on environment.
    
    Returns:
        int: Logging level (DEBUG for non-prod, ERROR for PROD)
    """
    environment = get_environment()
    
    if environment == 'PROD' or environment == 'PRODUCTION':
        return logging.ERROR
    else:
        # DEBUG for all other environments (STAGING, DEVELOPMENT, etc.)
        return logging.DEBUG


def get_log_format():
    """
    Get log format string based on environment.
    
    Production uses minimal format for performance.
    Non-production uses detailed format for debugging.
    
    Returns:
        str: Log format string
    """
    environment = get_environment()
    
    if environment == 'PROD' or environment == 'PRODUCTION':
        # Minimal format for production
        return '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    else:
        # Detailed format for debugging
        return '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(funcName)s() - %(message)s'


def setup_logging(
    log_file='app.log',
    max_bytes=10485760,  # 10MB
    backup_count=5,
    console_output=True
):
    """
    Configure logging for the application.
    
    Args:
        log_file (str): Path to log file
        max_bytes (int): Max size of log file before rotation (default: 10MB)
        backup_count (int): Number of backup log files to keep (default: 5)
        console_output (bool): Whether to output to console (default: True)
    
    Returns:
        logging.Logger: Configured root logger
    """
    log_level = get_log_level()
    log_format = get_log_format()
    environment = get_environment()
    
    # Create formatter
    formatter = logging.Formatter(log_format)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Remove existing handlers to avoid duplication
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Console handler
    if console_output:
        console_handler = logging.StreamHandler()
        console_handler.setLevel(log_level)
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)
    
    # File handler with rotation
    try:
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Warning: Could not setup file logging: {e}")
    
    # Log initialization info
    logger = logging.getLogger(__name__)
    logger.info(f"Logging initialized - Environment: {environment}, Level: {logging.getLevelName(log_level)}")
    
    return root_logger


def get_logger(name):
    """
    Get a logger instance with the given name.
    
    Args:
        name (str): Logger name (typically __name__)
    
    Returns:
        logging.Logger: Logger instance
    """
    return logging.getLogger(name)
