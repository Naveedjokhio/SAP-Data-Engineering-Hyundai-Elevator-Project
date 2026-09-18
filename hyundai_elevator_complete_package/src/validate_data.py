import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "hyundai_elevator_synthetic_data"

files = sorted(DATA_DIR.glob("*.csv"))

print("=" * 70)
print("HYUNDAI ELEVATOR - DATA VALIDATION")
print("=" * 70)
print(f"CSV files found: {len(files)}")
print()

for file in files:
    print("-" * 70)
    print(f"FILE: {file.name}")

    try:
        # Read only a sample first
        sample = pd.read_csv(file, nrows=5)

        # Count rows efficiently without loading entire file
        with open(file, "rb") as f:
            row_count = sum(1 for _ in f) - 1

        print(f"Rows     : {row_count:,}")
        print(f"Columns  : {len(sample.columns)}")
        print(f"Columns  : {', '.join(sample.columns)}")

        # Full validation only for smaller files
        if row_count <= 100000:
            df = pd.read_csv(file)

            print(f"Missing  : {df.isna().sum().sum():,}")
            print(f"Duplicates: {df.duplicated().sum():,}")

        else:
            print("Missing  : skipped (large file)")
            print("Duplicates: skipped (large file)")

    except Exception as e:
        print(f"ERROR: {e}")

print()
print("=" * 70)
print("VALIDATION COMPLETE")
print("=" * 70)
