import pandas as pd
from typing import Tuple
from src.utils.logger import get_logger

logger = get_logger(__name__)

def clean_tickets_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the customer support tickets dataset.
    - Fills or drops missing values in critical columns.
    - Normalizes text columns.
    
    Args:
        df: Raw DataFrame of support tickets.
        
    Returns:
        Cleaned pd.DataFrame.
    """
    logger.info("Starting data cleaning process.")
    
    # Make a copy to avoid SettingWithCopyWarning
    cleaned_df = df.copy()
    
    # Drop rows where 'Ticket Description' or 'Ticket Subject' is missing
    initial_shape = cleaned_df.shape
    cleaned_df.dropna(subset=['Ticket Description', 'Ticket Subject'], inplace=True)
    
    # Fill missing categorical values with 'Unknown'
    fill_unknown_cols = ['Customer Gender', 'Product Purchased', 'Ticket Type']
    for col in fill_unknown_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].fillna('Unknown')
            
    # Basic text normalization (strip whitespace)
    text_cols = ['Ticket Subject', 'Ticket Description']
    for col in text_cols:
        if col in cleaned_df.columns:
            cleaned_df[col] = cleaned_df[col].astype(str).str.strip()
            
    logger.info(f"Data cleaning complete. Dropped {initial_shape[0] - cleaned_df.shape[0]} rows due to missing critical data.")
    return cleaned_df

def prepare_features_labels(df: pd.DataFrame, text_col: str = 'Ticket Description', label_col: str = 'Ticket Priority') -> Tuple[pd.Series, pd.Series]:
    """
    Extracts features and labels for model training/inference.
    
    Args:
        df: Cleaned DataFrame.
        text_col: Name of the column containing the text feature.
        label_col: Name of the column containing the target label.
        
    Returns:
        Tuple of (X, y) as pandas Series.
    """
    if text_col not in df.columns or label_col not in df.columns:
        raise ValueError(f"Columns {text_col} or {label_col} not found in DataFrame.")
        
    # Drop rows where the label is missing
    valid_df = df.dropna(subset=[label_col]).copy()
    
    X = valid_df[text_col]
    y = valid_df[label_col]
    
    logger.info(f"Extracted {len(X)} samples for '{text_col}' and '{label_col}'.")
    return X, y
