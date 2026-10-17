
from utils.data_loader import (
    load_dataset,
    get_dataset_summary,
    list_available_datasets,
)

print("CLEAN CITY AI DATA LOADER TEST")
print("-" * 40)

for name, details in list_available_datasets().items():
    if details["exists"]:
        summary = get_dataset_summary(name)

        print(f"\nDataset: {name}")
        print(f"Rows: {summary['rows']}")
        print(f"Columns: {summary['columns']}")
        print(f"Missing values: {summary['missing_values']}")
    else:
        print(f"\nMISSING: {name}")

print("\nTest complete.")
