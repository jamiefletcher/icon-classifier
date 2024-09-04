import glob
import os.path
import re
import random

from PIL import Image, ImageOps, ImageFilter

SIZES = [(128, 128), (64, 64), (32, 32)]
F_COLOURS = ["red", "green", "blue", "orange", "yellow"]
BLUR_RANGE = (0.5, 1.5)

# Operations
def open(img_file_path: str) -> Image.Image:
    # Open RGBA images and convert to RGB with white background
    # https://stackoverflow.com/questions/9166400/convert-rgba-png-to-rgb-with-pil
    img = Image.open(img_file_path).convert("RGBA")
    img.load()
    img_bkgrnd = Image.new("RGB", img.size, (255, 255, 255))
    img_bkgrnd.paste(img, mask=img.split()[3]) # 3 is the apha channel
    return img_bkgrnd

def resize(img: Image.Image, size) -> Image.Image:
    return ImageOps.fit(img, size, Image.Resampling.LANCZOS)


def invert(img: Image.Image) -> Image.Image:
    return ImageOps.invert(img)


def recolour(img: Image.Image, black = "black", white="white") -> Image.Image:
    img_bw = img.convert("L")
    return ImageOps.colorize(img_bw, black=black, white=white)


def add_random_blur(img: Image.Image, bounds=(0,1)) -> Image.Image:
    g_stdev = random.uniform(bounds[0], bounds[1])
    return img.filter(ImageFilter.GaussianBlur(g_stdev))


def get_ref_num(filename: str) -> str:
    pattern = r"Ref-No_(.*?)\."
    result = re.search(pattern, filename)
    if result:
        return result.group(1).strip()
    return ""


def pipeline(img: Image.Image, add_blur = False) -> list[Image.Image]:
    variants = []

    for size in SIZES:
        img_resized = resize(img, size)
        for f_colour in F_COLOURS:
            variants.append(recolour(img_resized, black=f_colour))
            variants.append(recolour(img_resized, black=f_colour, white="black"))
        variants.append(img_resized)
        variants.append(invert(img_resized))

    if add_blur:
        return [add_random_blur(v, bounds=BLUR_RANGE) for v in variants]

    return variants


def process(input_folder: str, output_folder: str):
    for input_file in sorted(glob.glob(f"{input_folder}/*")):
        ref_num = get_ref_num(os.path.basename(input_file))
        img = open(input_file)
        img_variants = pipeline(img, add_blur=True)
        for i, ouput_img in enumerate(img_variants):
            output_file = f"{output_folder}/{ref_num}_{i}.png"
            ouput_img.save(output_file)
