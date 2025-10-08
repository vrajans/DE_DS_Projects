import camelot
import tabula
import pandas as pd
import re

#tables = camelot.read_pdf(r"D:\Medstar\nlem2022.pdf", pages="all", flavor="lattice")

# Extract tables across all pages
dfs = tabula.read_pdf(r"D:\Medstar\nlem2022.pdf", pages="all", multiple_tables=True,lattice=True)

#df_list = [t.df for t in tables]
merged = pd.concat(dfs, ignore_index=True)

merged = merged.dropna(how="all", axis=0)
#merged = merged.dropna(how="all", axis=1)

merged["raw"] = merged.astype(str).apply(lambda x: " ".join(x.dropna()), axis=1)

# expected_cols = ["Section", "Generic Name", "Dosage Form", "Strength", "Level"]
# merged.columns = (list(merged.columns[:len(expected_cols)]) + 
#                   expected_cols[len(merged.columns):])

def clean_text(x):
    if pd.isna(x):
        return ""
    x = str(x)
    # Remove known headers/footers
    x = re.sub(r"NLEM.*2022", "", x, flags=re.IGNORECASE)
    x = re.sub(r"Page\s*\d+", "", x, flags=re.IGNORECASE)
    return x.strip()

for col in merged.columns:
    merged[col] = merged[col].apply(clean_text)

# Step 6: Split combined fields if needed
# e.g., "Tablet 500 mg, 650 mg" → ["Tablet","500 mg"], ["Tablet","650 mg"]
clean_rows = []
for _, row in merged.iterrows():
    dosage = str(row.get("Dosage Form", ""))
    strength = str(row.get("Strength", ""))

    if "," in strength:  # multiple strengths
        for s in [x.strip() for x in strength.split(",")]:
            new_row = row.copy()
            new_row["Strength"] = s
            clean_rows.append(new_row)
    else:
        clean_rows.append(row)

cleaned_df = pd.DataFrame(clean_rows)

cleaned_df.to_csv(r"D:\Medstar\nlem_2022_merged.csv", index=False, encoding="utf-8-sig")

# for i, table in enumerate(tables):  
#     table.to_csv(f"table_{i}.csv")