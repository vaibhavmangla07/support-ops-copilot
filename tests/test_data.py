import pytest
import pandas as pd
from src.data.preprocessor import clean_tickets_data, prepare_features_labels

@pytest.fixture
def sample_raw_data():
    return pd.DataFrame({
        'Ticket Subject': ['Login Issue', None, '  Payment failed  '],
        'Ticket Description': ['Cannot login to account.', 'Blank subject', 'Card declined.'],
        'Ticket Type': ['Technical', 'General', None],
        'Ticket Priority': ['High', 'Low', 'Medium'],
        'Customer Gender': ['Male', 'Female', None]
    })

def test_clean_tickets_data(sample_raw_data):
    cleaned_df = clean_tickets_data(sample_raw_data)
    
    # Should drop row with missing subject
    assert len(cleaned_df) == 2
    
    # Should fill missing Ticket Type and Customer Gender
    assert 'Unknown' in cleaned_df['Ticket Type'].values
    assert 'Unknown' in cleaned_df['Customer Gender'].values
    
    # Should strip whitespace
    assert cleaned_df.iloc[1]['Ticket Subject'] == 'Payment failed'

def test_prepare_features_labels(sample_raw_data):
    cleaned_df = clean_tickets_data(sample_raw_data)
    X, y = prepare_features_labels(cleaned_df, text_col='Ticket Description', label_col='Ticket Priority')
    
    assert len(X) == 2
    assert len(y) == 2
    assert list(y.values) == ['High', 'Medium']

def test_prepare_features_labels_missing_cols(sample_raw_data):
    with pytest.raises(ValueError):
        prepare_features_labels(sample_raw_data, text_col='Nonexistent', label_col='Ticket Priority')
