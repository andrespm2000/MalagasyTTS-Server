from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

_instances = {}

def translate_text(text, lang_code, model_name):
    """
    Translates a given text into Malagasy using a pre-trained translation model.

    Args:
        texto (str): The input text to be translated.
        lang_code (str): The source language code of the input text (e.g., 'eng_Latn').

    Returns:
        str: The translated text in the target language.
    """
    if model_name in _instances:
        transTokenizer, transModel = _instances[model_name]
        print("Translation model loaded from cache")
    else:
        transTokenizer = AutoTokenizer.from_pretrained(model_name, src_lang=lang_code)
        transModel = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        print("Translation model downloaded")

    transInputs = transTokenizer(text, return_tensors="pt")
    with torch.no_grad():
        translatedTokens = transModel.generate(
            **transInputs,
            forced_bos_token_id=transTokenizer.convert_tokens_to_ids("plt_Latn"),
            max_length=512
        )
    _instances[model_name] = (transTokenizer, transModel)
    return transTokenizer.batch_decode(translatedTokens, skip_special_tokens=True)[0]