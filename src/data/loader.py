import pandas as pd
from pathlib import Path
from typing import Optional
from src.utils.logger import get_logger

logger = get_logger(__name__)

def load_data(filepath: str | Path) -> pd.DataFrame:
    """
    Loads dataset from a CSV file.
    
    Args:
        filepath: Path to the CSV file.
        
    Returns:
        pd.DataFrame containing the data.
        
    Raises:
        FileNotFoundError: If the file does not exist.
        pd.errors.EmptyDataError: If the file is empty.
    """
    path = Path(filepath)
    if not path.exists():
        logger.error(f"File not found: {path}")
        raise FileNotFoundError(f"File not found: {path}")
        
    try:
        logger.info(f"Loading data from {path}")
        df = pd.read_csv(path)
        logger.info(f"Successfully loaded {len(df)} rows and {len(df.columns)} columns.")
        return df
    except Exception as e:
        logger.error(f"Error loading data from {path}: {e}")
        raise
