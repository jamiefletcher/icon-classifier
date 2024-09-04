from download import download


def main():
    download(data_folder="data/raw/wikimedia", url_file="data/raw/wikimedia/urls.txt")


if __name__ == "__main__":
    main()
