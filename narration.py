from transformers import set_seed
import torch
import io
import soundfile as sf

def generate_audio(text, ttsModel, ttsTokenizer):
    """
    Generates an audio waveform from the given text using a pre-trained TTS model.

    Args:
        texto (str): The input text to be converted into speech.

    Returns:
        io.BytesIO: A buffer containing the generated audio in WAV format.
    """
    
    set_seed(555)
    ttsModel.to("cpu").eval()
    ttsInputs = ttsTokenizer(text, return_tensors="pt")
    with torch.no_grad():
        ttsOutput = ttsModel(**ttsInputs.to("cpu")).waveform[0]
    waveformNp = ttsOutput.cpu().float().numpy()

    #Saving audio to buffer
    audioBuffer = io.BytesIO()
    sf.write(audioBuffer, waveformNp, samplerate=ttsModel.config.sampling_rate, format="WAV")
    audioBuffer.seek(0)
    return audioBuffer