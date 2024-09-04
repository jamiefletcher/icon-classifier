import argparse

from download import download
from process import process


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

    # Parse the arguments and call appropriate function for the subcommand
    args = parser.parse_args()
    if args.command == "download":
        # download(data_folder="data/raw/wikimedia", url_file="data/raw/wikimedia/urls.txt")
        download(data_folder=args.data_folder, url_file=args.url_file)
    elif args.command == "process":
        process(input_folder=args.input_folder, output_folder=args.output_folder)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
