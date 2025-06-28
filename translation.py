from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

class Translator:
    def __init__(self):
        self._instances = {}
        self.currentTokenizer = None
        self.currentModel = None

    def getModel(self, model_name):
        """
        Retrieves the pre-trained model and tokenizer for translation.

        Args:
            model_name (str): The name of the pre-trained model to load.

        """
        if model_name in self._instances:
            self.currentTokenizer, self.currentModel = self._instances[model_name]
            print("Translation model loaded from cache")
        else:
            self.currentTokenizer = AutoTokenizer.from_pretrained(model_name)
            self.currentModel = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            print("Translation model downloaded")
            self._instances[model_name] = (self.currentTokenizer, self.currentModel)

    def translate_text(self, text, lang_code):
        """
        Translates a given text into Malagasy using a pre-trained translation model.

        Args:
            texto (str): The input text to be translated.
            lang_code (str): The source language code of the input text (e.g., 'eng_Latn').

        Returns:
            str: The translated text in the target language.
        """

        transInputs = self.currentTokenizer(text, return_tensors="pt")
        with torch.no_grad():
            translatedTokens = self.currentModel.generate(
                **transInputs,
                forced_bos_token_id=self.currentTokenizer.convert_tokens_to_ids("plt_Latn"),
                max_length=512
            )
        return self.currentTokenizer.batch_decode(translatedTokens, skip_special_tokens=True)[0]