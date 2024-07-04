from pathlib import Path
import sys

if __name__ == "__main__":
    src_path = Path(__file__).resolve().parent.parent / "src"
    sys.path.append(str(src_path))
    from main import scrape

    scrape(destination="College Station, TX, United States")
