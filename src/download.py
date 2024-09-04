import os.path
import re
import requests

headers = {'User-Agent': 'DashboardIconDownloadBot/0.0 (68712911+jamiefletcher@users.noreply.github.com)'}

class WikiIcon:
    def __init__(self, img_url: str, pixels=480):
        svg_filename = os.path.basename(img_url)
        png_filename = f"{pixels}px-{svg_filename}.png"
        self.filenames = [svg_filename, png_filename]
        self._img_urls = [
            ("svg", img_url),
            ("png", f"{img_url}/{png_filename}".replace("/commons", "/commons/thumb")),
        ]
        self._json_url = (
            "https://commons.wikimedia.org/w/api.php?action=query"
            "&prop=imageinfo"
            "&iiprop=extmetadata"
            f"&titles=File%3A{svg_filename}"
            "&format=json"
        )
        self.img_info = None

    def download(self, folder: str):
        for img_type, img_url in self._img_urls:
            filename = os.path.basename(img_url)
            r = requests.get(img_url, headers=headers)    
            with open(f"{folder}/{img_type}/{filename}", "wb") as fd:
                fd.write(r.content)

        r_json = requests.get(self._json_url, headers=headers).json()
        for page in r_json["query"]["pages"].values():
            self.img_info = page["imageinfo"][0]

    def meaning(self):
        description = self.img_info["extmetadata"]["ImageDescription"]["value"]
        pattern = r"Function/description:\s*(.*?)(<[^>]+>|\n|$)"
        result = re.search(pattern, description)
        if result:
            return result.group(1).strip()
        return ""