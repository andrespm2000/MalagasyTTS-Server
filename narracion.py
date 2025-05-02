from transformers import VitsTokenizer, VitsModel, set_seed
import torch
import io
import soundfile as sf

#TTS model and tokenizer loading
ttsModelName = "facebook/mms-tts-mlg"
ttsTokenizer = VitsTokenizer.from_pretrained(ttsModelName)
ttsModel = VitsModel.from_pretrained(ttsModelName)

def generar_audio(texto):
    """
    Generates an audio waveform from the given text using a pre-trained TTS model.

    Args:
        texto (str): The input text to be converted into speech.

    Returns:
        io.BytesIO: A buffer containing the generated audio in WAV format.
    """
    
    set_seed(555)
    ttsModel.to("cpu").eval()
    ttsInputs = ttsTokenizer(texto, return_tensors="pt")
    with torch.no_grad():
        ttsOutput = ttsModel(**ttsInputs.to("cpu")).waveform[0]
    waveformNp = ttsOutput.cpu().float().numpy()

    #Saving audio to buffer
    audioBuffer = io.BytesIO()
    sf.write(audioBuffer, waveformNp, samplerate=ttsModel.config.sampling_rate, format="WAV")
    audioBuffer.seek(0)
    return audioBuffer