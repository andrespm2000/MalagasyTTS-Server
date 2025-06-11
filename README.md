<a id="readme-top"></a>

[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]

<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="assets/icon.png" alt="Logo" width="80" height="80">
  </a>

  <h1 align="center">MalagasyTTS Server</h1>

  <p align="center">
    Backend server for the <a href="https://github.com/andrespm2000/MalagasyTTS-Extension">MalagasyTTS extension</a>
    <br />
    <a href="https://github.com/andrespm2000/MalagasyTTS-Server"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/andrespm2000/MalagasyTTS-Server/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    &middot;
    <a href="https://github.com/andrespm2000/MalagasyTTS-Server/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>

## About the project

This project provides a FastAPI-based server for the MalagasyTTS extension: Processing text input, detecting its language, translating it into Malagasy, and generating audio output using Text-to-Speech (TTS).

## How It Works

1. Model retrieval:

    - The detection, translation and TTS model URLs are passed to the corresponding module by calling their getModel function.
    - Each module will either retrieve the model form cache or download and cache it.

2. Language Detection:

    - The input text is passed to the detect_language function in detection.py.
    - The function uses the language detection model to identify the language and map it to a FLORES code.

3. Translation:

    - The detected language and input text are passed to the translate_text function in translation.py.
    - The function uses the translation model to translate the text into Malagasy.

4. Text-to-Speech:

    - The translated text is passed to the generate_audio function in narration.py.
    - The function uses the TTS model to generate audio from the text.

5. Response:

    - The server returns a multipart/mixed response containing the detected language, translated text, and the generated audio.

## File structure

- **main.py**: Main module. Runs the server API, handles requests and communication with the other modules.
- **detection.py**: Language detection module.
- **translation.py**: Translation to Malagasy module.
- **narration.py**: TTS generation module. 

## Built with
[![Python 3.12.9][python-logo]][python-url]
[![FastAPI][fastapi-logo]][fastapi-url]
[![Transformers][transformers-logo]][transformers-url]
[![PyTorch][pytorch-logo]][pytorch-url]
[![Docker][docker-logo]][docker-url]
<a href="https://www.uvicorn.org/"><img src="assets/uvicorn.png" alt="Uvicorn" width="60" style="vertical-align:middle" /></a>

## Installation

Make sure to have [Docker installed in your system](https://docs.docker.com/engine/install/)

1. Clone the repository:
   ```bash
   git clone https://github.com/andrespm2000/MalagasyTTS-Server/tree/main
   cd MalagasyTTSserver

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt

3. Build and run the Docker image (recommended):
    ```bash
    docker build -t <image name>:latest .
    docker run -d -p 8000:8000 --name <container name> <image name>:latest

4. Alternatively, manually run the server:
    ```bash
    uvicorn main:app --reload

5. In the case of having Nvidia GPUs available, build the image with Dockerfile-gpu:
    ```bash
    docker build -t <image name>:latest -f Dockerfile-gpu .
    docker run --gpus all -p 8000:8000 malagasytts --name <container name> <image name>:latest

## API Endpoints
- **GET /**
    - Description: A simple endpoint to test if the server is running.
    - Response: Returns an HTML page with a message.
- **POST /models**
    - Description: Processes the input text, detects its language translates it into Malagasy, and generates audio.
    - Request Parameters:
        - input (form-data): The text to process.
        - detModel (form-data): Detection model URL.
        - transModel (form-data): Translation model URL.
        - narrModel (form-data): Narration model URL.
    - Response: A multipart/mixed response containing:
        - Detected language and its FLORES code in JSON format.
        - The generated audio file in WAV format.

## Contact

Andrés Perdomo Martínez - [![LinkedIn][linkedin-shield]][linkedin-url] - andresperdomo737@gmail.com

<p align="right">(<a href="#readme-top">back to top</a>)</p>

[contributors-shield]: https://img.shields.io/github/contributors/andrespm2000/MalagasyTTS-Server.svg?style=for-the-badge
[contributors-url]: https://github.com/andrespm2000/MalagasyTTS-Server/graphs/contributors

[forks-shield]: https://img.shields.io/github/forks/andrespm2000/MalagasyTTS-Server.svg?style=for-the-badge
[forks-url]: https://github.com/andrespm2000/MalagasyTTS-Server/network/members

[stars-shield]: https://img.shields.io/github/stars/andrespm2000/MalagasyTTS-Server.svg?style=for-the-badge
[stars-url]: https://github.com/andrespm2000/MalagasyTTS-Server/stargazers

[issues-shield]: https://img.shields.io/github/issues/andrespm2000/MalagasyTTS-Server.svg?style=for-the-badge
[issues-url]: https://github.com/andrespm2000/MalagasyTTS-Server/issues

[linkedin-shield]: https://custom-icon-badges.demolab.com/badge/LinkedIn-0A66C2?logo=linkedin-white&logoColor=fff
[linkedin-url]: https://www.linkedin.com/in/andres-perdomo-12bb3b1ba/

[python-logo]:https://img.shields.io/badge/Python-3776AB?logo=python&logoColor=fff
[python-url]:https://www.python.org/downloads/release/python-3129/

[fastapi-logo]:https://img.shields.io/badge/FastAPI-009485.svg?logo=fastapi&logoColor=white
[fastapi-url]:https://fastapi.tiangolo.com/

[transformers-logo]:https://img.shields.io/badge/Hugging%20Face-FFD21E?logo=huggingface&logoColor=000
[transformers-url]:https://huggingface.co/docs/transformers/en/index

[pytorch-logo]:https://img.shields.io/badge/PyTorch-ee4c2c?logo=pytorch&logoColor=white
[pytorch-url]:https://pytorch.org/

[docker-logo]:https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=fff
[docker-url]:https://docs.docker.com/