from transformers import pipeline

MODEL_NAME="j-hartmann/emotion-english-distilroberta-base"
classifier = pipeline("text-classification", model=MODEL_NAME, return_all_scores=True)

classifier.save_pretrained(f"models/{MODEL_NAME}")
