import json

from datasets import load_from_disk
from sklearn.model_selection import KFold
from transformers import Trainer, TrainingArguments, ViTForImageClassification

from eval_model import compute_accuracy


def load_args(input_json: str):
    with open(input_json) as json_file:
        args = json.load(json_file)
    return args


def train(dataset_folder, training_args_json):
    # Load dataset
    dataset = load_from_disk(dataset_folder)
    labels = dataset["train"].features["label"].names

    # Load settings for the trainer
    json_args = load_args(training_args_json)

    pretrained_model = json_args["pretrained_model"]
    k_folds = json_args["k_folds"]
    training_args = TrainingArguments(**json_args["training_args"])
    results_folder = training_args.output_dir
    logs_folder = training_args.logging_dir 

    # Initialize with pre-trained model
    model = ViTForImageClassification.from_pretrained(
        pretrained_model,
        num_labels=len(labels),
        id2label={i: c for i, c in enumerate(labels)},
        label2id={c: i for i, c in enumerate(labels)},
        ignore_mismatched_sizes=True,  # Ignore the classifier's size mismatch
    )

    # Initialize k-fold splits
    kf = KFold(n_splits=k_folds, shuffle=True)

    # Perform k-fold training
    for fold, (train_idx, val_idx) in enumerate(kf.split(dataset["train"])):
        print(f"Training fold {fold+1}/{k_folds}")

        train_split = dataset["train"].select(train_idx)
        val_split = dataset["train"].select(val_idx)

        training_args.output_dir = f"{results_folder}/fold_{fold}"
        training_args.logging_dir = f"{logs_folder}/fold_{fold}"

        # Trainer instance for this fold
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_split,
            eval_dataset=val_split,
            compute_metrics=compute_accuracy,
        )
        trainer.train()
        trainer.evaluate()

    # Save model
    model.save_pretrained(f"{results_folder}/final_model")
