import pathlib
import csv


class CSV_storage:

    def __init__(self, destination, hotel_data, file_name):
        self.destination = destination
        self.hotel_data = hotel_data
        self.file_name = file_name

    def save_to_csv(self):
        if self.hotel_data:
            keys = self.hotel_data[0].keys()
            base_dir = (pathlib.Path(__file__).parent.parent.parent / "data" /
                        "raw" / self.destination)
            base_dir.mkdir(parents=True, exist_ok=True)

            file_path = base_dir / self.file_name
            print(file_path)

            with file_path.open("w", newline="") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.hotel_data)
