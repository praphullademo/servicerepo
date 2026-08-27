"""
Main application entry point demonstrating environment-based logging.
"""

from config import setup_logging, get_logger

# Initialize logging
setup_logging()

# Get logger for this module
logger = get_logger(__name__)


def main():
    """Main application function."""
    logger.debug("Starting application...")
    logger.debug("This debug message appears in non-prod environments only")
    
    logger.info("Application is running")
    logger.info("This info message appears in all environments")
    
    logger.warning("This is a warning message")
    logger.error("This error message appears in all environments")
    
    logger.debug("Application is shutting down...")
    print("Application completed successfully!")


if __name__ == '__main__':
    main()
