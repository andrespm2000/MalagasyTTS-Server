from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

_instances = {}

def detect_language(texto, langmap, model_name):
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
    
    if model_name in _instances:
        classifTokenizer, classifModel = _instances[model_name]
        print("Classification model loaded from cache")
    else:
        classifTokenizer = AutoTokenizer.from_pretrained(model_name)
        classifModel = AutoModelForSequenceClassification.from_pretrained(model_name)
        print("Classification model downloaded")
    
    classifInputs = classifTokenizer(texto, return_tensors="pt")
    with torch.no_grad():
        logits = classifModel(**classifInputs).logits
    predictedClassId = logits.argmax().item()
    detectedLang = classifModel.config.id2label[predictedClassId]
    _instances[model_name] = (classifTokenizer, classifModel)
    return detectedLang, langmap.get(detectedLang, "eng_Latn")