from transformers import set_seed, VitsTokenizer, VitsModel
import torch
import io
import soundfile as sf

_instances = {}
currentTokenizer = None
currentModel = None

def getModel(model_name):
    """
    Retrieves the pre-trained model and tokenizer for TTS.

    Args:
        model_name (str): The name of the pre-trained model to load.

    """
    global currentTokenizer, currentModel
    if model_name in _instances:
        currentTokenizer, currentModel = _instances[model_name]
        print("Classification model loaded from cache")
    else:
        currentTokenizer = VitsTokenizer.from_pretrained(model_name)
        currentModel = VitsModel.from_pretrained(model_name)
        print("Classification model downloaded")
        _instances[model_name] = (currentTokenizer, currentModel)

def generate_audio(text):
    """
    Generates an audio waveform from the given text using a pre-trained TTS model.

    Args:
        texto (str): The input text to be converted into speech.

    Returns:
        io.BytesIO: A buffer containing the generated audio in WAV format.
    """

    set_seed(555)
    currentModel.to("cpu").eval()
    ttsInputs = currentTokenizer(text, return_tensors="pt")
    with torch.no_grad():
        ttsOutput = currentModel(**ttsInputs.to("cpu")).waveform[0]
    waveformNp = ttsOutput.cpu().float().numpy()

    #Saving audio to buffer
    audioBuffer = io.BytesIO()
    sf.write(audioBuffer, waveformNp, samplerate=currentModel.config.sampling_rate, format="WAV")
    audioBuffer.seek(0)
    return audioBuffer