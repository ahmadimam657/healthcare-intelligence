"""
Logging Utility Module

Provides centralized logging configuration and logger instances for the project.
"""

import logging
import sys
from pathlib import Path


def setup_logger(name, log_file=None, level=logging.INFO):
    """
    Create and configure a logger instance.
    
    Args:
        name (str): Name of the logger (typically __name__)
        log_file (str or Path, optional): Path to log file. If None, logs to console only.
        level (int): Logging level (default: logging.INFO)
        
    Returns:
        logging.Logger: Configured logger instance
        
    Example:
        >>> from utils.logger_util import setup_logger
        >>> logger = setup_logger(__name__)
        >>> logger.info("This is an info message")
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding duplicate handlers
    if logger.hasHandlers():
        return logger
    
    # Log format
    log_format = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler (always add)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)
    
    # File handler (if log_file is provided)
    if log_file:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(level)
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)
    
    return logger


def get_project_root():
    """
    Get the project root directory.
    
    Returns:
        Path: Path object to the project root directory
    """
    return Path(__file__).parent.parent


def get_data_path(filename=""):
    """
    Get the path to a file in the data directory.
    
    Args:
        filename (str): Name of the file in the data directory
        
    Returns:
        Path: Path object to the file in data directory
    """
    data_dir = get_project_root() / "data"
    data_dir.mkdir(exist_ok=True)
    
    return data_dir / filename if filename else data_dir


def get_logs_path(filename=""):
    """
    Get the path to a file in the logs directory.
    
    Args:
        filename (str): Name of the file in the logs directory
        
    Returns:
        Path: Path object to the file in logs directory
    """
    logs_dir = get_project_root() / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    return logs_dir / filename if filename else logs_dir
