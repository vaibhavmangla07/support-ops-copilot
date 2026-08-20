import sys
import os

def check_environment():
    print("--- Environment Health Check ---")
    
    # 1. Python Version
    print(f"Python Version: {sys.version.split(' ')[0]}")
    if sys.version_info.major != 3 or sys.version_info.minor != 11:
        print("WARNING: Python version is not 3.11.x")
        
    print(f"Executable: {sys.executable}")
    
    # 2. Imports Verification
    libraries = [
        "numpy", "pandas", 
        "matplotlib", "seaborn", 
        "sklearn", "xgboost", 
        "torch", "optuna", 
        "nltk", "langchain", "langgraph", 
        "fastapi", "uvicorn", 
        "streamlit", "sqlite3"
    ]
    
    failed = []
    print("\n--- Core Library Import Check ---")
    for lib in libraries:
        try:
            __import__(lib)
            print(f"[OK] {lib}")
        except ImportError as e:
            print(f"[FAIL] {lib} - {e}")
            failed.append(lib)
            
    # 3. PyTorch Verification
    if "torch" not in failed:
        print("\n--- PyTorch Verification ---")
        try:
            import torch
            print(f"PyTorch Version: {torch.__version__}")
            x = torch.tensor([1.0, 2.0, 3.0])
            y = torch.tensor([4.0, 5.0, 6.0])
            z = x + y
            print(f"Tensor addition successful: {x} + {y} = {z}")
        except Exception as e:
            print(f"PyTorch verification failed: {e}")
            
    if failed:
        print("\n[!] Environment check completed with errors.")
        sys.exit(1)
    else:
        print("\n[+] Environment check completed successfully. All libraries present.")

if __name__ == "__main__":
    check_environment()
