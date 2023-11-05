import argparse

parser = argparse.ArgumentParser(description="CLI for ISL Transcription App")

command = parser.add_subparsers(dest="command", required=True)

command_create_dataset = command.add_parser(
    "combine-datasets", help="Combine the datasets"
)
command_create_dataset.add_argument(
    "--ratio", type=float, default=0.8, help="Train/Test split ratio"
)
command_create_dataset.add_argument(
    "--images-per-class", type=int, default=100, help="Number of images per class"
)

command_create_isl_model = command.add_parser(
    "create-isl-model", help="Create the ISL model"
)
command_create_isl_model.add_argument(
    "--model-path", type=str, default="model.keras", help="Path to save the model"
)
command_create_isl_model.add_argument(
    "--epochs", type=int, default=3, help="Epochs to train for"
)

command_test_isl_model = command.add_parser("test-isl-model", help="Test the ISL model")
command_test_isl_model.add_argument(
    "--model-path", type=str, default="model.keras", help="Path to load the model"
)

command_start_server = command.add_parser(
    "start-server", help="Start the FastAPI server."
)
command_start_server.add_argument(
    "--reload", help="Enable hot reload", action="store_true", default=False
)

command_create_landmarks_csv = command.add_parser(
    "create-landmarks-csv", help="Create landmarks csv"
)


def main():
    args = parser.parse_args()
    if args.command == "combine-datasets":
        from model.combine_datasets import combine_datasets

        combine_datasets(args)
    elif args.command == "create-isl-model":
        from model.create_isl_model import create_isl_model

        create_isl_model(args)
    elif args.command == "test-isl-model":
        from model.test_isl_model import test_isl_model

        test_isl_model(args)
    elif args.command == "start-server":
        from model.server import start_server

        start_server(args)
    elif args.command == "create-landmarks-csv":
        from model.hand_landmarks import create_landmarks_csv

        create_landmarks_csv(args)
