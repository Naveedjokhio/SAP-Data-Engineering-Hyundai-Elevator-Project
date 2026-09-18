import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "hyundai_elevator_synthetic_data"

primary_keys = {
    "Suppliers.csv": "supplier_id",
    "Materials.csv": "material_id",
    "PurchaseOrders.csv": "po_id",
    "PurchaseOrderItems.csv": "po_item_id",
    "Machines.csv": "machine_id",
    "ProductionOrders.csv": "production_order_id",
    "QualityInspections.csv": "inspection_id",
    "MachineDowntime.csv": "downtime_id",
    "Elevators.csv": "elevator_id",
    "ElevatorSensorData.csv": "sensor_record_id",
    "ElevatorAlarms.csv": "alarm_id",
    "Technicians.csv": "technician_id",
    "MaintenanceRecords.csv": "maintenance_id",
    "MaintenanceParts.csv": "maintenance_part_id",
    "ProductMapping.csv": "product_id"
}

print("=" * 70)
print("HYUNDAI ELEVATOR - PRIMARY KEY VALIDATION")
print("=" * 70)

all_pass = True

for filename, pk in primary_keys.items():

    file = DATA_DIR / filename

    df = pd.read_csv(file, usecols=[pk])

    duplicate_count = df[pk].duplicated().sum()
    null_count = df[pk].isna().sum()

    if duplicate_count == 0 and null_count == 0:
        print(f"[PASS] {filename}")
        print(f"       PK: {pk} | Rows: {len(df):,}")
    else:
        all_pass = False
        print(f"[FAIL] {filename}")
        print(f"       PK: {pk}")
        print(f"       Duplicates: {duplicate_count:,}")
        print(f"       Nulls: {null_count:,}")

print()
print("=" * 70)

if all_pass:
    print("ALL PRIMARY KEY CHECKS PASSED")
else:
    print("SOME PRIMARY KEY CHECKS FAILED")

print("=" * 70)
