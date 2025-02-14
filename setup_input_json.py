from pathlib import Path
import argparse
from src.preprocessing.guidelines import EntityGuidelines
from src.renal_biopsy.preprocessor import RenalBiopsyProcessor


def setup_input_json(guidelines_file: str, raw_data_file: str):
    # Define paths
    root_dir = Path("src/renal_biopsy")
    required_files = {
        "guidelines": root_dir / "data" / guidelines_file,
        "raw_data": root_dir / "data" / raw_data_file,
    }

    # Create input JSON
    eg = EntityGuidelines(required_files["guidelines"])
    processor = RenalBiopsyProcessor(guidelines=eg)
    _ = processor.create_input_json(
        data_path=required_files["raw_data"],
        save_path=root_dir / "data/real_input.json",
        full=True,
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--guidelines", default="guidelines.xlsx", help="Guidelines file name"
    )
    parser.add_argument(
        "--raw_data", default="synthetic_data.xlsx", help="Raw data file name"
    )
    args = parser.parse_args()

    setup_input_json(args.guidelines, args.raw_data)
