import os
import pandas as pd
import hashlib

def get_file_hash(filepath):
    """Calculate MD5 hash of a file to ensure integrity."""
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def validate_dataset(filepath):
    print(f"\n{'='*50}")
    print(f"Dataset: {os.path.basename(filepath)}")
    print(f"{'='*50}")
    
    if not os.path.exists(filepath):
        print("FILE NOT FOUND.")
        return
    
    # Task 1: Inventory
    filesize_mb = os.path.getsize(filepath) / (1024 * 1024)
    file_hash = get_file_hash(filepath)
    print(f"File Size: {filesize_mb:.2f} MB")
    print(f"MD5 Hash: {file_hash}")
    
    try:
        df = pd.read_csv(filepath, low_memory=False)
        print("Readable: Yes")
        print(f"Rows: {df.shape[0]}")
        print(f"Columns: {df.shape[1]}")
    except Exception as e:
        print(f"Readable: No. Error: {e}")
        return

    # Task 2 & 3: Schema & Data Quality
    print("\n--- Column Inspection ---")
    for col in df.columns:
        dtype = df[col].dtype
        missing_pct = df[col].isnull().sum() / len(df) * 100
        nunique = df[col].nunique()
        
        # Get a sample non-null value if possible
        sample_val = df[col].dropna().iloc[0] if not df[col].dropna().empty else None
        if isinstance(sample_val, str) and len(sample_val) > 50:
            sample_val = sample_val[:47] + "..."
            
        print(f"Column: {col} | Type: {dtype} | Unique: {nunique} | Missing: {missing_pct:.2f}%")
        print(f"  -> Sample: {sample_val}")
        
        # Basic quality checks
        if dtype == 'object':
            # Check empty strings
            empty_strings = (df[col] == "").sum()
            if empty_strings > 0:
                print(f"  -> WARNING: {empty_strings} empty strings")
                
    print("\n--- Row Quality ---")
    duplicates = df.duplicated().sum()
    print(f"Duplicate Rows: {duplicates} ({(duplicates/len(df)*100):.2f}%)")

def main():
    raw_dir = "datasets/raw/"
    if not os.path.exists(raw_dir):
        print(f"Directory {raw_dir} does not exist!")
        return
        
    print("Starting Dataset Validation Script...\n")
    datasets = [
        "aa_dataset-tickets-multi-lang-5-2-50-version.csv",
        "customer_support_tickets.csv"
    ]
    
    for ds in datasets:
        validate_dataset(os.path.join(raw_dir, ds))
        
    print("\nValidation complete. Raw data was not modified.")

if __name__ == "__main__":
    main()
