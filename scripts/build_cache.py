"""
Builds the consolidated analytical parquet cache from the raw CSVs.
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from services.data_loader import build_master_dataset, PARQUET_CACHE

def main():
    print("Building master analytical dataset from raw CSV tables...")
    t0 = time.time()
    df = build_master_dataset(use_parquet=False)
    duration = time.time() - t0
    print(f"Master dataset built in {duration:.2f}s!")
    print(f"Shape: {df.shape[0]:,} rows x {df.shape[1]} columns")
    print(f"Unique orders: {df['order_id'].nunique():,}")
    print(f"Unique customers: {df['customer_unique_id'].nunique():,}")
    print(f"Total Item Value: R$ {df['order_item_total'].sum():,.2f}")
    if os.path.exists(PARQUET_CACHE):
        print(f"Parquet cache saved: {PARQUET_CACHE} ({os.path.getsize(PARQUET_CACHE)/(1024*1024):.2f} MB)")

if __name__ == "__main__":
    main()
