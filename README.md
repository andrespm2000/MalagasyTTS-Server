# MalagasyTTS Server

This project provides a FastAPI-based server for processing text input, detecting its language, translating it into Malagasy, and generating audio output using Text-to-Speech (TTS). It integrates several pre-trained models from the Hugging Face Transformers library to perform language detection, translation, and speech synthesis.

## Features

- **Language Detection**: Automatically detects the language of the input text using a pre-trained language classification model.
- **Translation**: Translates the detected language into Malagasy using a pre-trained translation model.
- **Text-to-Speech (TTS)**: Converts the translated text into audio using a pre-trained TTS model.
- **API Endpoints**: Provides a RESTful API for easy integration with other applications.

## Models Used

1. **Language Detection**:
   - Model: `papluca/xlm-roberta-base-language-detection`
   - Purpose: Detects the language of the input text.

2. **Translation**:
   - Model: `facebook/nllb-200-distilled-600M`
   - Purpose: Translates the input text into Malagasy.

3. **Text-to-Speech (TTS)**:
   - Model: `facebook/mms-tts-mlg`
   - Purpose: Generates audio from the translated text.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd MalagasyTTSserver

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

3. Run the server:
    ```bash
    uvicorn main:app --reload

## API Endpoints
- **GET /**
    - Description: A simple endpoint to test if the server is running.
    - Response: Returns an HTML page with a message.
- **POST /models**
    - Description: Processes the input text, detects its language translates it into Malagasy, and generates audio.
    - Request Parameters:
        - input (form-data): The text to process.
    - Response: A multipart/mixed response containing:
        - Detected language and its FLORES code in JSON format.
        - The generated audio file in WAV format.

## How It Works

1. Language Detection:

    - The input text is passed to the detectar_idioma function in deteccion.py.
    - The function uses the language detection model to identify the language and map it to a FLORES code.

2. Translation:

    - The detected language and input text are passed to the traducir_texto function in traduccion.py.
    - The function uses the translation model to translate the text into Malagasy.

3. Text-to-Speech:

    - The translated text is passed to the generar_audio function in narracion.py.
    - The function uses the TTS model to generate audio from the text.

4. Response:

    - The server returns a multipart/mixed response containing the detected language, translated text, and the generated audio.

## Dependencies
- Python 3.8+
- [FastAPI](https://fastapi.tiangolo.com/)
- [Transformers](https://huggingface.co/transformers/)
- [PyTorch](https://pytorch.org/)

## Acknowledgments
- Hugging Face for providing pre-trained models.
- FastAPI for the web framework.
- PyTorch for the deep learning framework.