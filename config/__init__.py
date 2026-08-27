"""
Configuration package for the service.
"""

from .logging_config import setup_logging, get_logger, get_environment

__all__ = ['setup_logging', 'get_logger', 'get_environment']
