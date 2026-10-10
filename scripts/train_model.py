"""
Trains and saves the ML model artifacts.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.data_loader import build_master_dataset
from services.ml_service import train_and_evaluate_models

def main():
    print("Loading master dataset for ML training...")
    df = build_master_dataset()
    print(f"Master dataset: {df.shape[0]:,} rows")
    
    t0 = time.time()
    results = train_and_evaluate_models(df)
    duration = time.time() - t0
    print(f"Model training and evaluation finished in {duration:.2f}s!")
    print(f"Dataset unique customers: {results['dataset_size']:,}")
    print(f"Overall Churn Rate (single purchase): {results['churn_rate']:.2f}%")
    print("\nModel Comparison:")
    for name, metrics in results["models"].items():
        print(f"  [{name}]")
        print(f"    ROC-AUC:   {metrics.get('roc_auc', 0):.4f}")
        print(f"    F1 Score:  {metrics.get('f1', 0):.4f}")
        print(f"    Precision: {metrics.get('precision', 0):.4f}")
        print(f"    Recall:    {metrics.get('recall', 0):.4f}")
        print(f"    Accuracy:  {metrics.get('accuracy', 0):.4f}")

if __name__ == "__main__":
    main()
