import os

import torchvision.transforms as transforms
from datasets import ClassLabel, Dataset
from PIL import Image


# Define image transformation
# - Resize the image for ViT
# - Convert to a PyTorch tensor (C, H, W) with pixel values [0, 1]
# - Normalize pixel values to [-1, 1]
vit_transform = transforms.Compose(
    [
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5]),
    ]
)


def extract_label(filename):
    return filename.split("_")[0]  # label_XXX.png


def gather_image_paths(image_folder):
    images = []
    labels = []
    for filename in os.listdir(image_folder):
        if filename.endswith((".png", ".jpg", ".jpeg")):
            img_path = os.path.join(image_folder, filename)
            label = extract_label(filename)
            images.append(img_path)
            labels.append(label)
    return images, labels


def load_image(example, transform):
    image = Image.open(example["image"]).convert("RGB")
    example["pixel_values"] = transform(image)
    return example


def make_dataset(input_folder: str, output_folder: str, test_size=0.2):
    image_paths, all_labels = gather_image_paths(input_folder)

    # Create a Hugging Face dataset
    data = {"image": image_paths, "label": all_labels}
    dataset = Dataset.from_dict(data)
    dataset = dataset.map(lambda example: load_image(example, transform=vit_transform))

    # Create a ClassLabel feature
    labels = list(set(all_labels))
    class_labels = ClassLabel(names=labels)
    dataset = dataset.cast_column("label", class_labels)

    # Split train and test sets from full dataset
    if test_size > 0:
        dataset = dataset.train_test_split(
            test_size=test_size, stratify_by_column="label"
        )

    # Save dataset
    dataset.save_to_disk(output_folder)
