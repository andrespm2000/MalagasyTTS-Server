"""
Main module for the Malagasy TTS Server.

This module defines the FastAPI application, its endpoints, and the logic for processing
text input, detecting its language, translating it into Malagasy, and generating audio output.
"""

from fastapi import FastAPI, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from detection import detect_language
from translation import translate_text
from narration import generate_audio
from model_manager import ModelManager
import io

#Language code dictionary for translation
LANGMAP = {
  "ar": "arb_Arab",
  "bg": "bul_Cyrl",
  "de": "deu_Latn",
  "el": "ell_Grek",
  "en": "eng_Latn",
  "es": "spa_Latn",
  "fr": "fra_Latn",
  "hi": "hin_Deva",
  "it": "ita_Latn",
  "ja": "jpn_Jpan",
  "nl": "nld_Latn",
  "pl": "pol_Latn",
  "pt": "por_Latn",
  "ru": "rus_Cyrl",
  "sw": "swh_Latn",
  "th": "tha_Thai",
  "tr": "tur_Latn",
  "ur": "urd_Arab",
  "vi": "vie_Latn",
  "zh": "zho_Hans"
}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["Content-Type"],
)

#GET response for endpoint testing
@app.get("/", response_class=HTMLResponse)
async def root():
    """
    GET endpoint for testing if the server is running.

    Returns:
        HTMLResponse: A simple HTML page with a message.
    """

    return """
    <html>
        <head>
            <title>Wrong path</title>
        </head>
        <body>
            <h1>Wrong path ;)</h1>
        </body>
    </html>
    """

#POST request for data processing
@app.post("/models")
async def root(input: str = Form(...), detModel: str = Form(...), transModel: str = Form(...), narrModel: str = Form(...)):
    """
    POST endpoint for processing text input.

    Args:
        input (str): The text to process, provided as form-data.
        detModel (str): The name of the language detection model.
        transModel (str): The name of the translation model.
        narrModel (str): The name of the TTS model.

    Returns:
        StreamingResponse: A multipart/mixed response containing:
            - Detected language and its FLORES code in JSON format.
            - The generated audio file in WAV format.

    Raises:
        HTTPException: If the input text is empty.
    """

    print("Received input: ", input)

    #Empty text validation
    if input.__len__() == 0:
        raise HTTPException(status_code=400, detail="Text is empty")
    
    #Language detection
    classifModel, classifTokenizer = ModelManager.get_model(detModel, "classification")
    detectedLang, langTranslationCode = detect_language(input, LANGMAP, classifModel, classifTokenizer)
    
    #Translation
    transModelInstance, transTokenizer = ModelManager.get_model(transModel, "translation", lang_code=langTranslationCode)
    translatedText = translate_text(input, transModelInstance, transTokenizer)

    #TTS generation
    ttsModelInstance, ttsTokenizer = ModelManager.get_model(narrModel, "tts")
    audioBuffer = generate_audio(translatedText, ttsModelInstance, ttsTokenizer)
    
    #Response return
    boundary = "boundary123"
    response_content = (
        f"--{boundary}\r\n"
        "Content-Type: application/json\r\n\r\n"
        f'{{"detected_lang": "{detectedLang}", "flores_code": "{langTranslationCode}", "translated_text": "{translatedText}"}}\r\n'
        f"--{boundary}\r\n"
        "Content-Type: audio/wav\r\n"
        "Content-Disposition: attachment; filename=output.wav\r\n\r\n"
    ).encode("utf-8") + audioBuffer.read() + f"\r\n--{boundary}--\r\n".encode("utf-8")

    return StreamingResponse(io.BytesIO(response_content), media_type=f"multipart/mixed; boundary={boundary}")