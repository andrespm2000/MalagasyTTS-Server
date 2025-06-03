from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

_instances = {}
currentTokenizer = None
currentModel = None

def getModel(model_name):
    """
    Retrieves the pre-trained model and tokenizer for translation.

    Args:
        model_name (str): The name of the pre-trained model to load.

    """
    if model_name in _instances:
        currentTokenizer, currentModel = _instances[model_name]
        print("Classification model loaded from cache")
    else:
        currentTokenizer = AutoTokenizer.from_pretrained(model_name)
        currentModel = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        print("Classification model downloaded")
        _instances[model_name] = (currentTokenizer, currentModel)

def translate_text(text, lang_code):
    """
    Translates a given text into Malagasy using a pre-trained translation model.

    Args:
        texto (str): The input text to be translated.
        lang_code (str): The source language code of the input text (e.g., 'eng_Latn').

    Returns:
        str: The translated text in the target language.
    """

    transInputs = currentTokenizer(text, return_tensors="pt")
    with torch.no_grad():
        translatedTokens = currentModel.generate(
            **transInputs,
            forced_bos_token_id=currentTokenizer.convert_tokens_to_ids("plt_Latn"),
            max_length=512
        )
    return currentTokenizer.batch_decode(translatedTokens, skip_special_tokens=True)[0]