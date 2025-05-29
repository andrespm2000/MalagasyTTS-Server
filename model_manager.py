from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModelForSeq2SeqLM, VitsTokenizer, VitsModel

class ModelManager:
    _instances = {}

    @staticmethod
    def get_model(model_name, model_type, lang_code=None):
        """
        Retrieves a model and its tokenizer, downloading them if not cached.

        Args:
            model_name (str): The name of the model to load.
            model_type (str): The type of model ('classification', 'translation', 'tts').
            lang_code (str, optional): The source language code for translation models.

        Returns:
            tuple: A tuple containing the model and its tokenizer.
        """
        if model_name in ModelManager._instances:
            return ModelManager._instances[model_name]

        if model_type == "classification":
            tokenizer = AutoTokenizer.from_pretrained(model_name)
            model = AutoModelForSequenceClassification.from_pretrained(model_name)
        elif model_type == "translation":
            if lang_code is None:
                raise ValueError("lang_code must be provided for translation models")
            tokenizer = AutoTokenizer.from_pretrained(model_name, src_lang=lang_code)
            model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        elif model_type == "tts":
            tokenizer = VitsTokenizer.from_pretrained(model_name)
            model = VitsModel.from_pretrained(model_name)
        else:
            raise ValueError(f"Unknown model type: {model_type}")

        ModelManager._instances[model_name] = (model, tokenizer)
        return model, tokenizer