"""
Data Generation and Download Module

This module handles downloading the healthcare dataset from Kaggle
and moving it to the project's data directory.
"""

import sys
from pathlib import Path
import shutil
import os

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from dotenv import load_dotenv
import kagglehub
from utils.logging import setup_logger, get_data_path


def load_environment_variables():
    """
    Load environment variables from .env file.
    
    Returns:
        str: Kaggle API token from environment variables
        
    Raises:
        ValueError: If KAGGLE_API_TOKEN is not found in environment
    """
    logger.info("Loading environment variables from .env file")
    
    load_dotenv()
    
    token = os.getenv("KAGGLE_API_TOKEN")
    
    if not token:
        logger.error("KAGGLE_API_TOKEN not found in environment variables")
        raise ValueError(
            "KAGGLE_API_TOKEN not found in .env file. "
            "Please ensure .env contains your Kaggle API token."
        )
    
    logger.info("Environment variables loaded successfully")
    return token


def download_healthcare_dataset(dataset_name="prasad22/healthcare-dataset"):
    """
    Download healthcare dataset from Kaggle.
    
    Args:
        dataset_name (str): Kaggle dataset identifier.
                           Default: "prasad22/healthcare-dataset"
        
    Returns:
        Path: Path to the downloaded dataset directory
        
    Raises:
        Exception: If download fails
    """
    logger.info(f"Starting download of dataset: {dataset_name}")
    
    try:
        path = kagglehub.dataset_download(dataset_name)
        logger.info(f"Dataset downloaded successfully to: {path}")
        
        return Path(path)
    
    except Exception as e:
        logger.error(f"Failed to download dataset: {str(e)}", exc_info=True)
        raise


def copy_files_to_data_directory(src_path, dst_path=None):
    """
    Copy downloaded files from source to project's data directory.
    
    Args:
        src_path (Path): Source directory path where files were downloaded
        dst_path (Path, optional): Destination directory path. 
                                   If None, uses project's data directory.
        
    Returns:
        Path: Destination path where files were copied
    """
    if dst_path is None:
        dst_path = get_data_path()
    
    dst_path = Path(dst_path)
    
    logger.info(f"Copying files from {src_path} to {dst_path}")
    
    # Create data directory if it doesn't exist
    dst_path.mkdir(parents=True, exist_ok=True)
    logger.info(f"Ensured destination directory exists: {dst_path}")
    
    # Copy files and directories
    items_copied = 0
    try:
        for item in src_path.iterdir():
            target = dst_path / item.name
            
            if item.is_dir():
                logger.info(f"Copying directory: {item.name}")
                shutil.copytree(item, target, dirs_exist_ok=True)
            else:
                logger.info(f"Copying file: {item.name}")
                shutil.copy2(item, target)
            
            items_copied += 1
        
        logger.info(f"Successfully copied {items_copied} items to {dst_path}")
    
    except Exception as e:
        logger.error(f"Error copying files: {str(e)}", exc_info=True)
        raise
    
    return dst_path


def cleanup_source_directory(src_path):
    """
    Remove the source directory after files have been copied.
    
    Args:
        src_path (Path): Source directory path to remove
    """
    src_path = Path(src_path)
    
    logger.info(f"Cleaning up source directory: {src_path}")
    
    try:
        shutil.rmtree(src_path)
        logger.info(f"Source directory removed successfully: {src_path}")
    
    except Exception as e:
        logger.error(f"Failed to remove source directory: {str(e)}", exc_info=True)
        raise


def verify_data_downloaded(data_dir=None):
    """
    Verify that data files have been downloaded successfully.
    
    Args:
        data_dir (Path, optional): Data directory to check. 
                                   If None, uses project's data directory.
        
    Returns:
        bool: True if data files exist, False otherwise
    """
    if data_dir is None:
        data_dir = get_data_path()
    
    data_dir = Path(data_dir)
    
    logger.info(f"Verifying downloaded data in: {data_dir}")
    
    if not data_dir.exists():
        logger.error(f"Data directory does not exist: {data_dir}")
        return False
    
    files = list(data_dir.iterdir())
    
    if not files:
        logger.error(f"Data directory is empty: {data_dir}")
        return False
    
    logger.info(f"Found {len(files)} items in data directory:")
    for item in files:
        size = item.stat().st_size if item.is_file() else "directory"
        logger.info(f"  - {item.name} ({size})")
    
    return True


def generate_healthcare_data(dataset_name="prasad22/healthcare-dataset", 
                            cleanup=True):
    """
    Execute the complete data generation and download pipeline.
    
    Args:
        dataset_name (str): Kaggle dataset identifier.
                           Default: "prasad22/healthcare-dataset"
        cleanup (bool): Whether to clean up source directory after copying.
                       Default: True
        
    Returns:
        bool: True if data download and setup completed successfully
    """
    logger.info("=" * 60)
    logger.info("Starting Healthcare Data Generation Pipeline")
    logger.info("=" * 60)
    
    try:
        # Load environment variables
        load_environment_variables()
        
        # Download dataset from Kaggle
        src_path = download_healthcare_dataset(dataset_name)
        
        # Copy files to project's data directory
        dst_path = copy_files_to_data_directory(src_path)
        
        # Cleanup source directory
        if cleanup:
            cleanup_source_directory(src_path)
        else:
            logger.info(f"Skipping cleanup. Source directory remains at: {src_path}")
        
        # Verify data was downloaded
        if verify_data_downloaded(dst_path):
            logger.info("=" * 60)
            logger.info("Data Generation Pipeline Completed Successfully!")
            logger.info("=" * 60)
            return True
        else:
            logger.error("Data verification failed")
            return False
    
    except Exception as e:
        logger.error(f"Error in data generation pipeline: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    # Set up logger with file output
    from utils.logging import get_logs_path
    log_file = get_logs_path("generate_data.log")
    logger = setup_logger(__name__, log_file=str(log_file))
    
    logger.info(f"Log file: {log_file}")
    
    # Execute data generation pipeline
    success = generate_healthcare_data(
        dataset_name="prasad22/healthcare-dataset",
        cleanup=True
    )
    
    if success:
        logger.info("Ready to proceed with preprocessing")
    else:
        logger.error("Data generation failed")
        sys.exit(1)
