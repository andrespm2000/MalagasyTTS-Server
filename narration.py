from transformers import set_seed, VitsTokenizer, VitsModel
import torch
import io
import soundfile as sf

_instances = {}

def generate_audio(text, model_name):
    """
    Generates an audio waveform from the given text using a pre-trained TTS model.

    Args:
        texto (str): The input text to be converted into speech.

    Returns:
        io.BytesIO: A buffer containing the generated audio in WAV format.
    """
    
    if model_name in _instances:
        ttsTokenizer, ttsModel = _instances[model_name]
        print("Narration model loaded from cache")
    else:
        ttsTokenizer = VitsTokenizer.from_pretrained(model_name)
        ttsModel = VitsModel.from_pretrained(model_name)
        print("Narration model downloaded")

    set_seed(555)
    ttsModel.to("cpu").eval()
    ttsInputs = ttsTokenizer(text, return_tensors="pt")
    with torch.no_grad():
        ttsOutput = ttsModel(**ttsInputs.to("cpu")).waveform[0]
    waveformNp = ttsOutput.cpu().float().numpy()

    _instances[model_name] = (ttsTokenizer, ttsModel)

    #Saving audio to buffer
    audioBuffer = io.BytesIO()
    sf.write(audioBuffer, waveformNp, samplerate=ttsModel.config.sampling_rate, format="WAV")
    audioBuffer.seek(0)
    return audioBuffer