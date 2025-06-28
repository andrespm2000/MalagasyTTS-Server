from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class Detector:
    def __init__(self):
        self._instances = {}
        self.currentTokenizer = None
        self.currentModel = None

    def getModel(self, model_name):
        """
        Retrieves the pre-trained model and tokenizer for language detection.

        Args:
            model_name (str): The name of the pre-trained model to load.

        """
        if model_name in self._instances:
            self.currentTokenizer, self.currentModel = self._instances[model_name]
            print("Classification model loaded from cache")
        else:
            self.currentTokenizer = AutoTokenizer.from_pretrained(model_name)
            self.currentModel = AutoModelForSequenceClassification.from_pretrained(model_name)
            print("Classification model downloaded")
            self._instances[model_name] = (self.currentTokenizer, self.currentModel)

    def detect_language(self, texto, langmap):
        """
        Detects the language of a given text using a pre-trained language detection model.

        Args:
            texto (str): The input text whose language needs to be detected.
            langmap (dict): A dictionary mapping detected language codes to specific language identifiers.

        Returns:
            tuple: A tuple containing:
                - detectedLang (str): The detected language code (e.g., 'en', 'fr').
                - mappedLang (str): The corresponding language identifier from the langmap, 
                or "eng_Latn" if the detected language is not in the langmap.
        """
        
        classifInputs = self.currentTokenizer(texto, return_tensors="pt")
        with torch.no_grad():
            logits = self.currentModel(**classifInputs).logits
        predictedClassId = logits.argmax().item()
        detectedLang = self.currentModel.config.id2label[predictedClassId]
        return detectedLang, langmap.get(detectedLang, "eng_Latn")