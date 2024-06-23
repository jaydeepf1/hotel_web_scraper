import csv


def save_to_csv(data, filename='hotel_data.csv'):
    if data:
        keys = data[0].keys()
    
        # Write data to CSV file
        with open(filename, 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, fieldnames=keys)
            dict_writer.writeheader()
            dict_writer.writerows(data)
        
        print(f"Data saved to {filename}")
    else:
        print("No data to save")