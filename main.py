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
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

templates = Jinja2Templates(directory="templates")

# Fetch your OpenAI API key from the environment variable.

# todo: add openai key to .env file
# openai_key = os.getenv("OPENAI_API_KEY")
# if not openai_key:
#     raise Exception("Please set your OpenAI API key in the environment variable OPENAI_API_KEY.")

openai_key = os.getenv("OPENAI_API_KEY")
openai = OpenAI(api_key=openai_key)


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
async def process_form(request: Request, youtube_link: str = Form(...), prompt: str = Form("")):
    """
    Process the submitted YouTube link and prompt.
    """
    transcript_text = ""
    video_id = extract_video_id(youtube_link)
    if not video_id:
        return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid YouTube URL provided."})
    
    # Try to get the transcript from YouTube
    try:
        # manually break the try block and download the audio for better results
        err = 1/0
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = ", ".join([item['text'] for item in transcript_list])
    except Exception as e:
        # If no transcript found, download the audio and use OpenAI Whisper.
        try:
            yt = YouTube(youtube_link)
            audio_stream = yt.streams.get_audio_only()

            if not audio_stream:
                return templates.TemplateResponse("index.html", {"request": request, "error": "No audio stream available."})
            
            # Download audio to a temporary file.
            # with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_audio:
            #     audio_path = tmp_audio.name
            audio_path = 'data/'
            out_file = audio_stream.download(output_path=audio_path)
            # save the file
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            # If the mp3 file already exists, delete it.
            if os.path.exists(new_file):
                os.remove(new_file)
            os.rename(out_file, new_file)
            

            # Transcribe the audio using Whisper.
            with open(new_file, "rb") as audio_file:
                audio_transcript = openai.audio.transcriptions.create(
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

            response = openai.chat.completions.create(
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