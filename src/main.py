from download import WikiIcon
import json

def download(data_folder):    
    url_file = f"{data_folder}/urls.txt"
    json_file = f"{data_folder}/icon_descriptions.json"

    meanings = []

    with open(url_file, "r") as f:
        for url in f:
            w = WikiIcon(url.strip())
            w.download(data_folder)
            meanings.append({
                "files" : w.filenames,
                "meaning" : w.meaning()
            })
    
    with open(json_file, "w") as f:
        json.dump(meanings, f, indent=4)

def main():
    download(data_folder = "data/raw/wikimedia")

if __name__ == "__main__":
    main()