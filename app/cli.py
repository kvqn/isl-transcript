import argparse
from app.combine_datasets import combine_datasets

parser = argparse.ArgumentParser(description="CLI for ISL Transcription App")

command = parser.add_subparsers(dest="command", required=True)

command_create_dataset = command.add_parser("combine-datasets", help="Combine the datasets")
command_create_dataset.add_argument("--ratio", type=float, default=0.8, help="Train/Test split ratio")

def main():
    args = parser.parse_args()
    if args.command == "combine-datasets":
        combine_datasets(args)
