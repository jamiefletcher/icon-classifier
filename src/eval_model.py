import tempfile

import evaluate
import numpy as np
from datasets import load_from_disk
from transformers import Trainer, TrainingArguments, ViTForImageClassification

accuracy = evaluate.load("accuracy")


def compute_accuracy(p):
    pred = np.argmax(p.predictions, axis=1)
    lab = p.label_ids
    return accuracy.compute(predictions=pred, references=lab)


def eval_model(model_folder, dataset_folder):
    model = ViTForImageClassification.from_pretrained(model_folder)
    dataset = load_from_disk(dataset_folder)

    training_args = TrainingArguments(
        output_dir=tempfile.mkdtemp(),  # Dummy folder
        per_device_eval_batch_size=16,
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        eval_dataset=dataset["test"],
        compute_metrics=compute_accuracy,
    )

    print(f"Evaluation results: {trainer.evaluate()}")
