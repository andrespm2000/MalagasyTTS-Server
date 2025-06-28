from transformers import set_seed, VitsTokenizer, VitsModel
import torch
import io
import soundfile as sf

class Narrator:
    def __init__(self):
        self._instances = {}
        self.currentTokenizer = None
        self.currentModel = None

    def getModel(self, model_name):
        """
        Retrieves the pre-trained model and tokenizer for TTS.

        Args:
            model_name (str): The name of the pre-trained model to load.

        """
        if model_name in self._instances:
            self.currentTokenizer, self.currentModel = self._instances[model_name]
            print("Narration model loaded from cache")
        else:
            self.currentTokenizer = VitsTokenizer.from_pretrained(model_name)
            self.currentModel = VitsModel.from_pretrained(model_name)
            print("Narration model downloaded")
            self._instances[model_name] = (self.currentTokenizer, self.currentModel)

    def generate_audio(self, text):
        """
        Generates an audio waveform from the given text using a pre-trained TTS model.

        Args:
            texto (str): The input text to be converted into speech.

        Returns:
            io.BytesIO: A buffer containing the generated audio in WAV format.
        """

        set_seed(555)
        self.currentModel.to("cpu").eval()
        ttsInputs = self.currentTokenizer(text, return_tensors="pt")
        with torch.no_grad():
            ttsOutput = self.currentModel(**ttsInputs.to("cpu")).waveform[0]
        waveformNp = ttsOutput.cpu().float().numpy()

        #Saving audio to buffer
        audioBuffer = io.BytesIO()
        sf.write(audioBuffer, waveformNp, samplerate=self.currentModel.config.sampling_rate, format="WAV")
        audioBuffer.seek(0)
        return audioBuffer