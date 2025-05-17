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
    allow_origins=["*"],  # Change this to the frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze_sales_call")
async def analyze_sales_call(file: UploadFile = File(...)):
    temp_file_path = "temp_audio.m4a"

    try:
        # Step 1: Save the uploaded file temporarily
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Step 2: Transcribe the audio using Whisper
        with open(temp_file_path, "rb") as audio_file:
            transcript = openai.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1"
            )

        os.remove(temp_file_path)

        transcription_text = transcript.text

        # Step 3: Friendly analysis using GPT
        prompt = f"""
You're a supportive and encouraging sales coach.

Please analyze the following sales call and provide friendly, constructive feedback directly to the salesperson. Focus on what they did well, areas they can improve, and give specific, practical tips to help them boost their sales performance.

Your response should be:
- Empathetic and motivating
- Easy to understand
- Actionable and not too formal

Transcript:
\"\"\"
{transcription_text}
\"\"\"
"""

        response = openai.chat.completions.create(
            model="gpt-4",  # Use gpt-3.5-turbo if preferred
            messages=[
                {"role": "system", "content": "You are a professional sales coach who gives supportive feedback."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )

        analysis = response.choices[0].message.content

        return {
            "transcription": transcription_text,
            "analysis": analysis
        }

    except Exception as e:
        print(f"Error during transcription or analysis: {e}")
        raise HTTPException(status_code=500, detail="Processing failed")
