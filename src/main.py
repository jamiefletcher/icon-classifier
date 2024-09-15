import argparse

from download import download
from process import process
from make_dataset import make_dataset
from eval_model import eval_model
from train import train

def main():
    parser = argparse.ArgumentParser(
        description="An image classifier for ISO 2575 dashboad indicator icons."
    )
    subparsers = parser.add_subparsers(dest="command", help="Sub-command help")

    # Subparser for the 'download' command
    parser_download = subparsers.add_parser(
        "download", help="Download ISO 2575 icons from Wikimedia"
    )
    parser_download.add_argument(
        "--data_folder", required=True, help="Folder path for saving icons"
    )
    parser_download.add_argument(
        "--url_file", required=True, help="File with list of icon urls to download"
    )

    # Subparser for the 'process' command
    parser_process = subparsers.add_parser("process", help="Process data")
    parser_process.add_argument(
        "--input_folder", required=True, help="Folder path for loading downloaded icons"
    )
    parser_process.add_argument(
        "--output_folder", required=True, help="Folder path for saving processed icons"
    )

    # Subparser for the 'make-ds' command
    parser_process = subparsers.add_parser("make-ds", help="Make dataset")
    parser_process.add_argument(
        "--input_folder", required=True, help="Folder path for loading processed icons"
    )
    parser_process.add_argument(
        "--output_folder", required=True, help="Folder path for saving Hugging Face dataset"
    )
    parser_process.add_argument(
        "--test_size", required=False, type=float, default=0.2, help="Percent of dataset to reserve for test set"
    )

    # Subparser for the 'train' command
    parser_process = subparsers.add_parser("train", help="Train model on dataset with k-folds cross-validation")
    parser_process.add_argument(
        "--dataset", required=True, help="Folder path for loading Hugging Face dataset"
    )
    parser_process.add_argument(
        "--json_args", required=True, help="File path for loading JSON file with training arguments"
    )

    # Subparser for the 'evaluate' command
    parser_process = subparsers.add_parser("evaluate", help="Evaluate model on test dataset")
    parser_process.add_argument(
        "--model", required=True, help="Folder path for loading saved model"
    )
    parser_process.add_argument(
        "--dataset", required=True, help="Folder path for loading Hugging Face dataset"
    )

    # Parse the arguments and call appropriate function for the subcommand
    args = parser.parse_args()
    if args.command == "download":
        download(data_folder=args.data_folder, url_file=args.url_file)
    elif args.command == "process":
        process(input_folder=args.input_folder, output_folder=args.output_folder)
    elif args.command == "make-ds":
        make_dataset(input_folder=args.input_folder, output_folder=args.output_folder, test_size=args.test_size)
    elif args.command == "train":
        train(dataset_folder=args.dataset, training_args_json=args.json_args)
    elif args.command == "evaluate":
        eval_model(model_folder=args.model, dataset_folder=args.dataset)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
