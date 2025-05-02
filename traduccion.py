from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
import torch

#Translation model and tokenizer loading
transModelName = "facebook/nllb-200-distilled-600M"
transModel = AutoModelForSeq2SeqLM.from_pretrained(transModelName)

def traducir_texto(texto, lang_code):
    """
    Translates a given text into Malagasy using a pre-trained translation model.

    Args:
        texto (str): The input text to be translated.
        lang_code (str): The source language code of the input text (e.g., 'eng_Latn').

    Returns:
        str: The translated text in the target language.
    """

    transTokenizer = AutoTokenizer.from_pretrained(transModelName, src_lang=lang_code)
    transInputs = transTokenizer(texto, return_tensors="pt")
    with torch.no_grad():
        translatedTokens = transModel.generate(
            **transInputs,
            forced_bos_token_id=transTokenizer.convert_tokens_to_ids("plt_Latn"),
            max_length=512
        )
    return transTokenizer.batch_decode(translatedTokens, skip_special_tokens=True)[0]