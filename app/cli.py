import argparse

from app.dataset.create import combine_datasets

parser = argparse.ArgumentParser(description="CLI for ISL Transcription App")

command = parser.add_subparsers(dest="command", required=True)

command_create_dataset = command.add_parser("combine-datasets", help="Combine the datasets")


def main():
    args = parser.parse_args()
    if args.command == "combine-datasets":
        combine_datasets(args)
