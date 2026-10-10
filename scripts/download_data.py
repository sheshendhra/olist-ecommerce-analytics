"""
Script to download Olist Brazilian E-Commerce dataset from public repository.
Provides the 8 analytical tables needed for complete sales, customer, delivery,
SQL, and ML analysis.
"""
import os
import urllib.request
import time

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")

FILES = [
    "olist_orders_dataset.csv",
    "olist_order_items_dataset.csv",
    "olist_customers_dataset.csv",
    "olist_order_payments_dataset.csv",
    "olist_order_reviews_dataset.csv",
    "olist_products_dataset.csv",
    "olist_sellers_dataset.csv",
    "product_category_name_translation.csv"
]

BASE_URL = "https://raw.githubusercontent.com/ChinhMaiGit/Project-SQL-1/main/data"

def download_all(force=False):
    os.makedirs(DATA_DIR, exist_ok=True)
    print(f"Target data directory: {DATA_DIR}")
    for fname in FILES:
        target_path = os.path.join(DATA_DIR, fname)
        if os.path.exists(target_path) and not force and os.path.getsize(target_path) > 1000:
            print(f"  [ALREADY EXISTS] {fname} ({os.path.getsize(target_path):,} bytes)")
            continue
        
        url = f"{BASE_URL}/{fname}"
        print(f"  Downloading {fname} from {url}...")
        t0 = time.time()
        try:
            urllib.request.urlretrieve(url, target_path)
            size = os.path.getsize(target_path)
            duration = time.time() - t0
            print(f"  [OK] {fname}: {size:,} bytes downloaded in {duration:.1f}s")
        except Exception as e:
            print(f"  [ERROR] Failed to download {fname}: {e}")

if __name__ == "__main__":
    download_all()
