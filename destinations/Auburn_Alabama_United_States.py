from pathlib import Path
import sys

if __name__ == "__main__":
    src_path = Path(__file__).resolve().parent.parent / "src"
    sys.path.append(str(src_path))
    from main import scrape

    scrape(destination="Auburn, Alabama, United States")
    # from src.storage.csv_storage import CSV_storage

    # CSV_storage("a", [{"a": 1}], "x").save_to_csv()
