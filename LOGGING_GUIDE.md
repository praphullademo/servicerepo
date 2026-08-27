# Logging Configuration Guide

This guide explains how to use the environment-based logging system in this service.

## Overview

The logging system automatically adjusts verbosity based on the deployment environment:

- **PROD/PRODUCTION**: Only ERROR level messages are logged (minimal output)
- **All other environments** (DEVELOPMENT, STAGING, etc.): DEBUG level messages are logged (detailed output)

## Setup

### 1. Initialize Logging in Your Application

In your main application file, import and initialize logging at startup:

```python
from config import setup_logging, get_logger

# Initialize logging (do this once at application startup)
setup_logging()

# Get logger for your module
logger = get_logger(__name__)
```

### 2. Set Environment Variable

Configure the `ENVIRONMENT` variable for your deployment:

```bash
# For development (default if not set)
export ENVIRONMENT=DEVELOPMENT

# For production
export ENVIRONMENT=PRODUCTION

# For staging
export ENVIRONMENT=STAGING
```

Or create a `.env` file:

```
ENVIRONMENT=PRODUCTION
```

### 3. Use Logger Throughout Your Code

```python
from config import get_logger

logger = get_logger(__name__)

def process_request(request_id):
    logger.debug(f"Processing request: {request_id}")  # Only in non-prod
    logger.info(f"Request started: {request_id}")      # Always logged
    
    try:
        # do something
        logger.debug("Operation succeeded")             # Only in non-prod
    except Exception as e:
        logger.error(f"Failed to process request: {e}") # Always logged
```

## Logging Levels

The logging system supports the standard Python logging levels:

| Level | When to Use | Prod | Non-Prod |
|-------|------------|------|----------|
| **DEBUG** | Detailed diagnostic info for developers | ✗ | ✓ |
| **INFO** | Confirmation that things are working | ✓ | ✓ |
| **WARNING** | Something unexpected (still working) | ✓ | ✓ |
| **ERROR** | A serious problem occurred | ✓ | ✓ |
| **CRITICAL** | Very serious problem (urgent action needed) | ✓ | ✓ |

## Best Practices

1. **Use DEBUG for detailed diagnostics**
   ```python
   logger.debug(f"Variable state: {state}")
   logger.debug(f"Processing with options: {options}")
   ```

2. **Use INFO for important business events**
   ```python
   logger.info(f"User {user_id} logged in")
   logger.info(f"Order {order_id} completed")
   ```

3. **Use WARNING for recoverable issues**
   ```python
   logger.warning(f"Retry attempt {attempt} for request {request_id}")
   logger.warning(f"Cache miss for key: {key}")
   ```

4. **Use ERROR for failures that need attention**
   ```python
   logger.error(f"Database connection failed: {error}")
   logger.error(f"Payment processing failed for order {order_id}: {error}")
   ```

5. **Include context in log messages**
   ```python
   # Good: includes context
   logger.error(f"Failed to fetch user {user_id} from database: {error}")
   
   # Avoid: vague message
   logger.error(f"Error occurred: {error}")
   ```

## Log Output

### Console Output

Logs are printed to console with the following format:

**Production (ERROR level only):**
```
2026-08-27 10:30:45,123 - mymodule - ERROR - Database connection failed
```

**Non-Production (DEBUG level with detailed info):**
```
2026-08-27 10:30:45,123 - mymodule - DEBUG - [database.py:45] - connect() - Attempting connection to localhost:5432
```

### File Output

Logs are also written to `app.log` with automatic rotation:
- **Max file size**: 10MB (rotates to `app.log.1`, `app.log.2`, etc.)
- **Backup files kept**: 5 previous rotated logs

## Configuration

To customize logging behavior, modify `setup_logging()` call in your application:

```python
setup_logging(
    log_file='logs/service.log',      # Custom log file path
    max_bytes=5242880,                 # Rotate at 5MB instead of 10MB
    backup_count=10,                   # Keep 10 backup files instead of 5
    console_output=True                # Enable/disable console output
)
```

## Troubleshooting

**Logs not appearing?**
- Check that `setup_logging()` is called early in application startup
- Verify `ENVIRONMENT` variable is set correctly
- Ensure you're using `get_logger(__name__)` to get logger instances

**Too many logs in production?**
- Verify `ENVIRONMENT=PRODUCTION` is set
- Check that no code is using `logging.DEBUG` level directly
- Use appropriate log levels (ERROR/WARNING, not DEBUG/INFO)

**Log file not created?**
- Check file system permissions for the log directory
- Verify the directory exists or can be created
- Check available disk space
