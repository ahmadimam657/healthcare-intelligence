"""
Healthcare Data Preprocessing Pipeline

This module handles the loading, cleaning, and preprocessing of healthcare data.
It performs the following operations:
- Remove unnecessary columns
- Standardize categorical values and names
- Convert date columns to datetime format
- Calculate length of stay
- Remove duplicates
- Detect and handle invalid values
- One-hot encode categorical variables
- Save preprocessed data to CSV
"""

import sys
from pathlib import Path
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import json


# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from utils.logging import get_data_path

def load_data(input_file):
    """
    Load healthcare data from CSV file.
    
    Args:
        input_file (str): Name of the input CSV file in the data directory
        
    Returns:
        pd.DataFrame: Loaded dataframe
        
    Raises:
        FileNotFoundError: If the input file doesn't exist
    """
    file_path = get_data_path(input_file)
    
    if not file_path.exists():
        logger.error(f"Input file not found: {file_path}")
        raise FileNotFoundError(f"Input file not found: {file_path}")
    
    logger.info(f"Loading data from {file_path}")
    df = pd.read_csv(file_path)
    logger.info(f"Data loaded successfully. Shape: {df.shape}")
    
    return df


def remove_unnecessary_columns(df):
    """
    Remove unnecessary columns from the dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with unnecessary columns removed
    """
    columns_to_drop = ['Room Number', 'Insurance Provider']
    
    logger.info(f"Removing columns: {columns_to_drop}")
    df = df.drop(columns_to_drop, axis=1)
    
    logger.info(f"Remaining columns: {list(df.columns)}")
    
    return df


def standardize_categorical_values(df):
    """
    Standardize categorical values by converting to lowercase and stripping whitespace.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with standardized categorical values
    """
    logger.info("Standardizing categorical values (lowercase, strip whitespace)")
    
    object_columns = df.select_dtypes(include=['object', 'string']).columns
    
    for col in object_columns:
        df[col] = df[col].str.strip().str.lower()
    
    logger.info(f"Standardized {len(object_columns)} categorical columns")
    
    return df


def convert_date_columns(df):
    """
    Convert date columns to datetime format and calculate length of stay.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with datetime columns and length of stay calculated
    """
    logger.info("Converting date columns to datetime format")
    
    df['Date of Admission'] = pd.to_datetime(df['Date of Admission'])
    df['Discharge Date'] = pd.to_datetime(df['Discharge Date'])
    
    logger.info("Calculating length of stay (in days)")
    df['Length of Stay'] = (df['Discharge Date'] - df['Date of Admission']).dt.days
    
    logger.info(f"Length of Stay range: {df['Length of Stay'].min()} to {df['Length of Stay'].max()} days")
    
    return df


def check_missing_values(df):
    """
    Check and log missing values in the dataframe.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        dict: Dictionary of columns and their missing value counts
    """
    logger.info("Checking for missing values")
    
    missing_values = df.isnull().sum()
    missing_dict = missing_values[missing_values > 0].to_dict()
    
    if missing_dict:
        logger.warning(f"Missing values found: {missing_dict}")
    else:
        logger.info("No missing values detected")
    
    return missing_dict


def remove_duplicates(df):
    """
    Detect and remove duplicate rows.
    
    Args:
        df (pd.DataFrame): Input dataframe
        
    Returns:
        pd.DataFrame: Dataframe with duplicates removed
    """
    duplicates_before = df.duplicated().sum()
    logger.info(f"Number of duplicate rows before removal: {duplicates_before}")
    
    df = df.drop_duplicates()
    
    duplicates_after = df.duplicated().sum()
    logger.info(f"Number of duplicate rows after removal: {duplicates_after}")
    
    return df


def check_data_quality(df):
    """
    Check for impossible or invalid values in numeric columns.
    
    Args:
        df (pd.DataFrame): Input dataframe
    """
    logger.info("Checking data quality")
    
    # Check for negative billing amounts
    negative_billing = (df['Billing Amount'] < 0).sum()
    if negative_billing > 0:
        logger.warning(f"Found {negative_billing} rows with negative billing amounts")
    
    # Check for invalid ages
    invalid_ages = ((df['Age'] < 0) | (df['Age'] > 120)).sum()
    if invalid_ages > 0:
        logger.warning(f"Found {invalid_ages} rows with invalid ages")
    
    # Log data statistics
    logger.info("\n=== Data Statistics ===")
    logger.info(f"Age - Min: {df['Age'].min()}, Max: {df['Age'].max()}, Mean: {df['Age'].mean():.2f}")
    logger.info(f"Billing Amount - Min: ${df['Billing Amount'].min():.2f}, Max: ${df['Billing Amount'].max():.2f}, Mean: ${df['Billing Amount'].mean():.2f}")
    logger.info(f"Length of Stay - Min: {df['Length of Stay'].min()}, Max: {df['Length of Stay'].max()}, Mean: {df['Length of Stay'].mean():.2f} days")

#  In our case, we will use Label Encoding for categorical variables to convert them into numerical format.
#  This is suitable for algorithms that can interpret ordinal relationships, and it helps in reducing the dimensionality of the dataset
#  compared to one-hot encoding.
def label_encode(df, save_mappings=True):
    """
    Label encode categorical variables and save mappings.
    
    Args:
        df (pd.DataFrame): Input dataframe
        save_mappings (bool): Whether to save encoding mappings as JSON files
        
    Returns:
        pd.DataFrame: Dataframe with label encoded categorical variables
    """
    columns_to_encode = ['Gender', 'Blood Type', 'Medical Condition', 'Test Results',
                         'Admission Type', 'Medication', 'Doctor', 'Hospital']
    
    logger.info(f"Label encoding columns: {columns_to_encode}")
    
    for col in columns_to_encode:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        
        if save_mappings:
            # Create mapping: original -> encoded
            mapping = dict(zip(le.classes_.tolist(), range(len(le.classes_))))
            
            file_path = get_data_path(f"encodings/{col}_mapping.json")
            file_path.parent.mkdir(exist_ok=True)
            
            # Save only the mapping we need
            with open(file_path, 'w') as f:
                json.dump(mapping, f, indent=2)
            
            logger.info(f"Saved mapping for {col}: {len(mapping)} values")
    
    logger.info(f"Encoding complete. Shape: {df.shape}")
    
    return df


def save_preprocessed_data(df, output_file):
    """
    Save preprocessed data to CSV file.
    
    Args:
        df (pd.DataFrame): Preprocessed dataframe
        output_file (str): Name of the output CSV file to save in data directory
    """
    file_path = get_data_path(output_file)
    
    logger.info(f"Saving preprocessed data to {file_path}")
    df.to_csv(file_path, index=False)
    
    logger.info(f"Data saved successfully. Final shape: {df.shape}")
    logger.info(f"File size: {file_path.stat().st_size / (1024*1024):.2f} MB")


def preprocess_healthcare_data(input_file="healthcare_dataset.csv", 
                              output_file="preprocessed_healthcare_dataset.csv",
                              log_file=None):
    """
    Execute the complete healthcare data preprocessing pipeline.
    
    Args:
        input_file (str): Name of the input CSV file in the data directory.
                         Default: "healthcare_dataset.csv"
        output_file (str): Name of the output CSV file to save in data directory.
                          Default: "preprocessed_healthcare_dataset.csv"
        log_file (str, optional): Path to log file. If None, logs to console only.
        
    Returns:
        pd.DataFrame: Preprocessed dataframe
    """
    logger.info("=" * 60)
    logger.info("Starting Healthcare Data Preprocessing Pipeline")
    logger.info("=" * 60)
    
    try:
        # Load data
        df = load_data(input_file)
        
        # Remove unnecessary columns
        df = remove_unnecessary_columns(df)
        
        # Standardize categorical values
        df = standardize_categorical_values(df)
        
        # Convert date columns
        df = convert_date_columns(df)
        
        # Check missing values
        check_missing_values(df)
        
        # Remove duplicates
        df = remove_duplicates(df)
        
        # Check data quality
        check_data_quality(df)
        
        # Label encode categorical variables
        df = label_encode(df)
        
        # Save preprocessed data
        save_preprocessed_data(df, output_file)
        
        logger.info("=" * 60)
        logger.info("Preprocessing Pipeline Completed Successfully!")
        logger.info("=" * 60)
        
        return df
    
    except Exception as e:
        logger.error(f"Error in preprocessing pipeline: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    from utils.logging import get_logs_path, setup_logger
    
    log_file = get_logs_path("preprocessing.log")
    logger = setup_logger(__name__, log_file=str(log_file))

    # Execute preprocessing pipeline
    df = preprocess_healthcare_data(
        input_file="healthcare_dataset.csv",
        output_file="preprocessed_healthcare_dataset.csv",
        log_file="preprocessing.log"
    )
