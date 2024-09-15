# icon-classifier
Dashboard icon classifier in Python using vision transformers

This is a spin-off project from another research project where large vision language models (LVLMs) were used to generate descriptions of icons that appear on vehicle dashboards. That work was [presented](docs/LUSRC2024_poster.pdf) at the [Lassonde Undergraduate Summer Research Conference 2024](https://lassonde.yorku.ca/research/lassonde-undergraduate-research-conference-2024-2), where it won first place!

## Motivation

The visual designs of vehicle dashboard icons are standardized by [ISO 2575](https://www.iso.org/obp/ui/#iso:std:iso:2575:ed-9:v1:en), which is a subset of [ISO 7000](https://www.iso.org/obp/ui/#iso:pub:PUB400001:en). One of the challenges with processing icons from actual vehicle manuals is that vehicle manufacturers make minor cosmetic changes to the icons, which causes them to deviate from the standard. This causes some duplication when building up a dataset of icons and their descriptions.

The goal here is to train a model on the ISO standard icon designs and then to use this model to classify icons found in vehicle manuals. The model is based on a pre-trained vision transformer model that is fine-tuned on dashboard icon images.

## Challenges

- Attempts to use classical computer vision methods (e.g. correlation, structural similarity, ...) to match ISO icons with actual dashboard icons were not very successful (<10% accuracy).

- Most of the large image datasets (e.g. ImageNet, MS COCO, ...) contain natural images whereas dashboard icons are drawings.

- The number of unique dashboard icons used in a single manual is typically quite small (30-40 icons) and certainly much smaller than the 300+ icons in the ISO standard.

## What's in here?

This repository contains:

- **data/raw** Free versions of ISO icons, which are available from the [Wikimedia Commons](https://commons.wikimedia.org/wiki/Category:Dashboard_SVG_icons)

- **data/processed** Processed versions of the free ISO icons. These icons have been rescaled, recoloured and otherwise adjusted to boost the size of the dataset.

- **src** Python source code for icon downloading, pre-processing, model training and evaluation.

- **notebooks** Python notebooks for prototyping and data exploration.

## Usage

The `src/main.py` script can be run directly from the command line. The following subcommands are implemented:

**Downloading icons from Wikimedia**
```
python src/main.py download --data_folder=data/raw/wikimedia --url_file=data/raw/wikimedia/urls.txt
```

**Pre-processing the icon images**
```
python src/main.py process --input_folder=data/processed/selected --output_folder=data/processed/variants
```

**Making a Hugging Face dataset from the processed icon images**
```
python src/main.py make-ds --input_folder="data/processed/variants" --output_folder="data/processed/huggingface" --test_size=0.2
```

**Train icon image classifier using k-folds cross-validation**
```
python src/main.py train --dataset="data/processed/huggingface" --json_args="src/training_args.json"
```

**Evaluate classifier on test dataset**
```
python src/main.py evaluate --model="models/results/final_model" --dataset="data/processed/huggingface"
```
