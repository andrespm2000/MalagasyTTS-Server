import torch

def detect_language(texto, langmap, classifModel, classifTokenizer):
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
    
    classifInputs = classifTokenizer(texto, return_tensors="pt")
    with torch.no_grad():
        logits = classifModel(**classifInputs).logits
    predictedClassId = logits.argmax().item()
    detectedLang = classifModel.config.id2label[predictedClassId]
    return detectedLang, langmap.get(detectedLang, "eng_Latn")