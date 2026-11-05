import pandas as pd
import glob
import os

# Merge all monthly sales reports
all_data = pd.DataFrame()

for f in glob.glob("reports/*.xlsx"):
    df = pd.read_excel(f)
    all_data = all_data.append(df, ignore_index=True)

# Sort by date
all_data = all_data.sort_values("date")

# Write output
os.makedirs("output", exist_ok=True)
writer = pd.ExcelWriter("output/merged_sales.xlsx")
all_data.to_excel(writer, sheet_name="Sales", index=False)
writer.save()

print(f"Merged {len(all_data)} rows into output/merged_sales.xlsx")
