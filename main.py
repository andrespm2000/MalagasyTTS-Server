"""
Main module for the Malagasy TTS Server.

This module defines the FastAPI application, its endpoints, and the logic for processing
text input, detecting its language, translating it into Malagasy, and generating audio output.
"""

from fastapi import FastAPI, Form, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse, HTMLResponse
from deteccion import classifModel, classifTokenizer, detectar_idioma
from traduccion import transModel, traducir_texto
from narracion import ttsModel, ttsTokenizer, generar_audio
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

# Model and tokenizer loading
print("Downloading models...")
_ = classifModel, classifTokenizer  # Language detection
_ = transModel  # Translation
_ = ttsModel, ttsTokenizer  # TTS
print("Models downloaded successfully.")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["chrome-extension://hpllhjddcjiiemjndbapegfijfgdpjlh",
                   "chrome-extension://jplhbppcnijfhohdcpoolfadkaaglgpb",
                   "moz-extension://5ac6b05f-45a5-4903-91cc-4e7cbc9c3208"],
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
async def root(input:str = Form(...)):
    """
    POST endpoint for processing text input.

    Args:
        input (str): The text to process, provided as form-data.

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
    detectedLang, langTranslationCode = detectar_idioma(input, LANGMAP)
    
    #Translation
    translatedText = traducir_texto(input, langTranslationCode)

    #TTS generation
    audioBuffer = generar_audio(translatedText)
    
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