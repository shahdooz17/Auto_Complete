import pandas as pd

# Load your CSV file
df = pd.read_csv("data/arabic_dataset_classifiction.csv")

# Drop rows with nulls in any column
df_cleaned = df.dropna()

# Extract only the first column (by index or name)
first_column = df_cleaned.iloc[:, 0]

# Save to .txt file (one line per entry)
first_column.to_csv("arabic_cleaned_data.txt", index=False, header=False)
