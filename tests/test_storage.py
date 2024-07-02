import unittest
import pathlib
import csv
import os
from tempfile import TemporaryDirectory
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
            base_dir = (
                pathlib.Path(__file__).parent.parent.parent
                / "data"
                / "processed"
                / self.destination
            )
            base_dir.mkdir(parents=True, exist_ok=True)

            file_path = base_dir / self.file_name
            print(file_path)

            with file_path.open("w", newline="") as output_file:
                dict_writer = csv.DictWriter(output_file, fieldnames=keys)
                dict_writer.writeheader()
                dict_writer.writerows(self.hotel_data)


class TestCSVStorage(unittest.TestCase):

    def setUp(self):
        self.test_data = [
            {
                "hotel_name": "Hotel A",
                "check_in": "2024-07-01",
                "check_out": "2024-07-05",
            },
            {
                "hotel_name": "Hotel B",
                "check_in": "2024-07-10",
                "check_out": "2024-07-15",
            },
        ]
        self.destination = "test_destination"
        self.file_name = "test_hotels.csv"

        # Create a temporary directory for testing
        self.test_dir = TemporaryDirectory()
        self.test_base_path = pathlib.Path(self.test_dir.name)

        # Mock the __file__ attribute
        self.original_file = globals().get("__file__")
        globals()["__file__"] = str(self.test_base_path / "mock_script.py")

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

        # Restore the original __file__ attribute
        if self.original_file is not None:
            globals()["__file__"] = self.original_file

    def test_save_to_csv(self):
        csv_storage = CSV_storage(self.destination, self.test_data, self.file_name)
        csv_storage.save_to_csv()

        expected_file_path = (
            self.test_base_path
            / "data"
            / "processed"
            / self.destination
            / self.file_name
        )
        self.assertTrue(
            expected_file_path.exists(), f"File {expected_file_path} does not exist."
        )

        with expected_file_path.open() as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertEqual(
                len(rows),
                len(self.test_data),
                "Number of rows in CSV does not match the input data.",
            )
            for i, row in enumerate(rows):
                self.assertDictEqual(
                    row,
                    self.test_data[i],
                    f"Row {i} in CSV does not match the input data.",
                )


if __name__ == "__main__":
    unittest.main()
