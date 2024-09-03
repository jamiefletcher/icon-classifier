from download import WikiIcon

def main():
    wi_test = WikiIcon("https://upload.wikimedia.org/wikipedia/commons/1/13/ISO_7000_-_Ref-No_0082.svg")
    print(wi_test.filenames)

    wi_test.download(folder="data/raw/wikimedia")

    print(wi_test.meaning())

if __name__ == "__main__":
    main()