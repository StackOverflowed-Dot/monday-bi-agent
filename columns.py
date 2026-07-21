from monday_client import load_all_data

deals, work = load_all_data()

print("DEALS COLUMNS")
print(deals.columns.tolist())

print("\nWORK ORDER COLUMNS")
print(work.columns.tolist())