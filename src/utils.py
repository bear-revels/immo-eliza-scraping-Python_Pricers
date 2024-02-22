import csv

def write_dictlist_to_csv(data, csv_file):
    filtered_data = [row for row in data if row is not None]  # Filter out None values
    if filtered_data:
        with open(csv_file, 'w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=filtered_data[0].keys())
            writer.writeheader()
            writer.writerows(filtered_data)
        print(f'Data has been written to {csv_file}')
    else:
        print("No data to write.")
