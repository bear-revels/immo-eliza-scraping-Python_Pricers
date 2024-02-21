import pandas as pd

# Load the CSV file. Pandas handles the issue of closing the file, so no with open... needed
df = pd.read_csv('merged_data.csv')  # dataset with 5k items
# Looking for duplicates based on the 'ID' column
duplicates_by_id = df[df.duplicated(subset='ID', keep=False)]
# Extracting the 'ID' and 'PropertyUrl' for duplicates found
duplicates_id_info = duplicates_by_id[['ID', 'PropertyUrl']]

# Save these to new CSV files
duplicates_id_info.to_csv('duplicates_by_id.csv', index=False)
print('Duplicates search finished')