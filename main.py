from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from youtube_transcript_api import YouTubeTranscriptApi
from pytubefix import YouTube
from pytubefix.cli import on_progress
from openai import OpenAI
import os
import tempfile
import re

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Fetch your OpenAI API key from the environment variable.
# todo: add openai key to .env file
# openai_key = os.getenv("OPENAI_API_KEY")
# if not openai_key:
#     raise Exception("Please set your OpenAI API key in the environment variable OPENAI_API_KEY.")

def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats.
    """
    regex_list = [
        r"(?<=v=)[^&#]+",     # For URLs like https://www.youtube.com/watch?v=VIDEOID
        r"(?<=be/)[^&#?]+",   # For URLs like https://youtu.be/VIDEOID
        r"(?<=embed/)[^&#?]+",# For URLs like https://www.youtube.com/embed/VIDEOID
    ]
    for regex in regex_list:
        match = re.search(regex, url)
        if match:
            return match.group(0)
    return None

@app.get("/", response_class=HTMLResponse)
async def read_form(request: Request):
    """
    Render the main form page.
    """
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/", response_class=HTMLResponse)
async def process_form(
    request: Request, 
    youtube_link: str = Form(...), 
    prompt: str = Form(""),
    openai_api_key: str = Form("")  # new field for OpenAI API key
):
    """
    Process the submitted YouTube link and prompt.
    """
    transcript_text = ""
    # Get the OpenAI API key from the submitted form or fallback to environment variable.
    key = openai_api_key.strip() or os.getenv("OPENAI_API_KEY")
    if not key:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": "Please provide your OpenAI API key in the API key field or set it in your environment variable."}
        )
    # Create an OpenAI client using the provided/found key.
    client = OpenAI(api_key=key)
    
    video_id = extract_video_id(youtube_link)
    if not video_id:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": "Invalid YouTube URL provided."}
        )
    
    # Try to get the transcript from YouTube
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ", ".join([item['text'] for item in transcript_list])
    except Exception as e:
        # If no transcript found, download audio and use Whisper.
        try:
            yt = YouTube(youtube_link)
            audio_stream = yt.streams.get_audio_only()
            if not audio_stream:
                return templates.TemplateResponse(
                    "index.html", 
                    {"request": request, "error": "No audio stream available."}
                )
            
            audio_path = 'data/'
            out_file = audio_stream.download(output_path=audio_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            if os.path.exists(new_file):
                os.remove(new_file)
            os.rename(out_file, new_file)
            
            # Transcribe the audio using Whisper.
            with open(new_file, "rb") as audio_file:
                audio_transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                transcript_text = audio_transcript.text
            
            # Cleanup the temporary audio file.
            os.remove(new_file)
        except Exception as inner_e:
            return templates.TemplateResponse(
                "index.html", 
                {"request": request, "error": f"Error extracting transcript: {str(inner_e)}"}
            )
    
    try:
        if prompt.strip() == "":
            result_text = None
        else:
            messages = [
                {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript_text}"}
            ]
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=0.7,
            )
            result_text = response.choices[0].message.content.strip()
    except Exception as e:
        return templates.TemplateResponse(
            "index.html", 
            {"request": request, "error": f"Error during OpenAI completion: {str(e)}"}
        )
    
    return templates.TemplateResponse(
        "index.html", 
        {"request": request, "result": result_text, "transcript": transcript_text}
    ) 