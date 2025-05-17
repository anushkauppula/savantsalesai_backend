import os
import openai
import shutil
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend origin in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    temp_file_path = "temp_audio.m4a"

    try:
        # Save uploaded audio file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Open file for transcription
        with open(temp_file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )

        os.remove(temp_file_path)
        return {"transcription": transcript.text}

    except Exception as e:
        # Log the error for debugging
        print(f"Error during transcription: {e}")
        # Raise HTTP error for client
        raise HTTPException(status_code=500, detail="Transcription failed")
