import pandas as pd
import json

file1 = "../dataset/customer_support_tickets.csv"
file2 = "../dataset/aa_dataset-tickets-multi-lang-5-2-50-version.csv"

def analyze_csv(filepath):
    try:
        df = pd.read_csv(filepath)
        info = {
            "file": filepath,
            "shape": df.shape,
            "columns": list(df.columns),
            "sample": df.head(1).to_dict(orient="records")[0] if not df.empty else {}
        }
        return info
    except Exception as e:
        return {"file": filepath, "error": str(e)}

if __name__ == "__main__":
    out1 = analyze_csv(file1)
    out2 = analyze_csv(file2)
    with open("eda_output.json", "w") as f:
        json.dump([out1, out2], f, indent=2, default=str)
