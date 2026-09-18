import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "hyundai_elevator_synthetic_data"

expected = {
    "Suppliers.csv": 100,
    "Materials.csv": 300,
    "PurchaseOrders.csv": 5000,
    "PurchaseOrderItems.csv": 10000,
    "Machines.csv": 50,
    "ProductionOrders.csv": 20000,
    "QualityInspections.csv": 20000,
    "MachineDowntime.csv": 5000,
    "Elevators.csv": 500,
    "ElevatorSensorData.csv": 1000000,
    "ElevatorAlarms.csv": 20000,
    "Technicians.csv": 100,
    "MaintenanceRecords.csv": 30000,
    "MaintenanceParts.csv": 50000,
    "ProductMapping.csv": None
}

print("=" * 70)
print("HYUNDAI ELEVATOR - ROW COUNT VALIDATION")
print("=" * 70)

for filename, expected_rows in expected.items():

    file = DATA_DIR / filename

    if not file.exists():
        print(f"[MISSING] {filename}")
        continue

    print(f"\nChecking: {filename}")

    # Count rows without loading the complete dataset
    with open(file, "r", encoding="utf-8-sig", errors="ignore") as f:
        rows = sum(1 for _ in f) - 1

    print(f"Actual rows   : {rows:,}")

    if expected_rows is None:
        print("Expected rows : Not fixed")
        print("Status        : OK")
    elif rows == expected_rows:
        print(f"Expected rows : {expected_rows:,}")
        print("Status        : PASS")
    else:
        print(f"Expected rows : {expected_rows:,}")
        print("Status        : FAIL")

print("\n" + "=" * 70)
print("ROW COUNT CHECK COMPLETE")
print("=" * 70)
