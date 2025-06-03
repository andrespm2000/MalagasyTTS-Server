from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

_instances = {}
currentTokenizer = None
currentModel = None

def getModel(model_name):
    """
    Retrieves the pre-trained model and tokenizer for language detection.

    Args:
        model_name (str): The name of the pre-trained model to load.

    """
    if model_name in _instances:
        currentTokenizer, currentModel = _instances[model_name]
        print("Classification model loaded from cache")
    else:
        currentTokenizer = AutoTokenizer.from_pretrained(model_name)
        currentModel = AutoModelForSequenceClassification.from_pretrained(model_name)
        print("Classification model downloaded")
        _instances[model_name] = (currentTokenizer, currentModel)

def detect_language(texto, langmap):
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
    
    classifInputs = currentTokenizer(texto, return_tensors="pt")
    with torch.no_grad():
        logits = currentModel(**classifInputs).logits
    predictedClassId = logits.argmax().item()
    detectedLang = currentModel.config.id2label[predictedClassId]
    return detectedLang, langmap.get(detectedLang, "eng_Latn")