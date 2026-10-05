import os
import pandas as pd

DATASETS = ["datasets/raw/aa_dataset-tickets-multi-lang-5-2-50-version.csv", "datasets/raw/customer_support_tickets.csv"]

for file in DATASETS:
    print(f"\nChecking: {file}")
    if not os.path.exists(file):
        print("File not found")
        continue

    try:
        df = pd.read_csv(file, low_memory=False)
        print("File readable")
        print("Rows:", df.shape[0])
        print("Columns:", df.shape[1])
        print("Duplicate rows:", df.duplicated().sum())
        print("Missing values:", df.isnull().sum().sum())

    except Exception as e:
        print("Could not read file")
        print("Error:", e)