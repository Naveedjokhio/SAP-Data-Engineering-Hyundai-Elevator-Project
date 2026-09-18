import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "hyundai_elevator_synthetic_data"

checks = [
    ("Materials.csv", "supplier_id", "Suppliers.csv", "supplier_id"),
    ("PurchaseOrders.csv", "supplier_id", "Suppliers.csv", "supplier_id"),
    ("PurchaseOrderItems.csv", "po_id", "PurchaseOrders.csv", "po_id"),
    ("PurchaseOrderItems.csv", "material_id", "Materials.csv", "material_id"),
    ("ProductionOrders.csv", "machine_id", "Machines.csv", "machine_id"),
    ("QualityInspections.csv", "production_order_id", "ProductionOrders.csv", "production_order_id"),
    ("MachineDowntime.csv", "machine_id", "Machines.csv", "machine_id"),
    ("MachineDowntime.csv", "production_order_id", "ProductionOrders.csv", "production_order_id"),
    ("ElevatorSensorData.csv", "elevator_id", "Elevators.csv", "elevator_id"),
    ("ElevatorAlarms.csv", "elevator_id", "Elevators.csv", "elevator_id"),
    ("MaintenanceRecords.csv", "elevator_id", "Elevators.csv", "elevator_id"),
    ("MaintenanceRecords.csv", "technician_id", "Technicians.csv", "technician_id"),
    ("MaintenanceParts.csv", "maintenance_id", "MaintenanceRecords.csv", "maintenance_id"),
    ("MaintenanceParts.csv", "material_id", "Materials.csv", "material_id"),
]

print("=" * 75)
print("HYUNDAI ELEVATOR - FOREIGN KEY VALIDATION")
print("=" * 75)

all_pass = True

for child_file, child_col, parent_file, parent_col in checks:

    child = pd.read_csv(DATA_DIR / child_file, usecols=[child_col])
    parent = pd.read_csv(DATA_DIR / parent_file, usecols=[parent_col])

    child_values = set(child[child_col].dropna().astype(str))
    parent_values = set(parent[parent_col].dropna().astype(str))

    broken = child_values - parent_values

    if len(broken) == 0:
        print(f"[PASS] {child_file}.{child_col} -> {parent_file}.{parent_col}")
    else:
        all_pass = False
        print(f"[FAIL] {child_file}.{child_col} -> {parent_file}.{parent_col}")
        print(f"       Broken FK values: {len(broken)}")
        print(f"       Examples: {list(broken)[:5]}")

print()
print("=" * 75)

if all_pass:
    print("ALL FOREIGN KEY CHECKS PASSED")
else:
    print("SOME FOREIGN KEY CHECKS FAILED")

print("=" * 75)
