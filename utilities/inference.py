import csv
import os
import re
import tempfile
from youtube_transcript_api import YouTubeTranscriptApi
from pytubefix import YouTube
from pytubefix.cli import on_progress
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables and setup the OpenAI client.
load_dotenv()
openai_key = os.getenv("OPENAI_API_KEY")
if not openai_key:
    raise Exception("Please set your OpenAI API key in the environment variable OPENAI_API_KEY.")
openai = OpenAI(api_key=openai_key)

# Define a fixed prompt for generating the summary.
SUMMARY_PROMPT = "Please provide a concise summary of the video transcript in a few sentences."

def extract_video_id(url: str) -> str:
    """
    Extract YouTube video ID from various URL formats.
    """
    regex_list = [
        r"(?<=v=)[^&#]+",     # e.g. https://www.youtube.com/watch?v=VIDEOID
        r"(?<=be/)[^&#?]+",   # e.g. https://youtu.be/VIDEOID
        r"(?<=embed/)[^&#?]+",# e.g. https://www.youtube.com/embed/VIDEOID
    ]
    for regex in regex_list:
        match = re.search(regex, url)
        if match:
            return match.group(0)
    return None

def get_transcript(youtube_link: str, video_id: str) -> str:
    """
    Attempt to get the transcript using the YouTubeTranscriptApi.
    If it fails, download the audio, and use OpenAI's Whisper to transcribe.
    """
    transcript_text = ""
    try:
        d = 1/0
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([item['text'] for item in transcript_list])
    except Exception as e:
        # Fallback to downloading audio and using Whisper transcription.
        try:
            yt = YouTube(youtube_link)
            audio_stream = yt.streams.get_audio_only()
            if not audio_stream:
                raise Exception("No audio stream available.")
            
            # Ensure that the 'data/' directory exists.
            os.makedirs("data/", exist_ok=True)
            audio_path = 'data/'
            out_file = audio_stream.download(output_path=audio_path)
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            # If the mp3 file already exists, remove it.
            if os.path.exists(new_file):
                os.remove(new_file)
            os.rename(out_file, new_file)
            
            # Use Whisper via OpenAI to transcribe the audio.
            with open(new_file, "rb") as audio_file:
                audio_transcript = openai.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
            transcript_text = audio_transcript.text
            # Cleanup the temporary audio file.
            os.remove(new_file)
        except Exception as inner_e:
            transcript_text = f"Error extracting transcript: {str(inner_e)}"
    return transcript_text

def get_summary(transcript_text: str, prompt=SUMMARY_PROMPT) -> str:
    """
    Use OpenAI chat completion to generate a summary, using transcript text and a fixed prompt.
    """
    try:
        # If the transcript is empty or indicates an error, skip summary.
        if transcript_text.strip() == "" or transcript_text.startswith("Error"):
            return ""
        messages = [
            {"role": "user", "content": f"{prompt}\n\nTranscript:\n{transcript_text}"}
        ]
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
            temperature=0.7,
        )
        summary = response.choices[0].message.content.strip()
        return summary
    except Exception as e:
        return f"Error during summary generation: {str(e)}"

def main():
    input_csv = "yt_links.csv"       # Original CSV with YT Link and Texture Description columns.
    # input_csv = "yt_links_copy.csv"       # Original CSV with YT Link and Texture Description columns.
    output_csv = "yt_links_processed.csv"  # New CSV with added Summary and Transcript columns.
    
    with open(input_csv, "r", newline='', encoding="utf-8") as infile, \
         open(output_csv, "w", newline='', encoding="utf-8") as outfile:
        
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames + ["Summary", "Transcript"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        
        count = 1
        for row in reader:
            youtube_link = row["YT Link"]
            print(f"Count: {count}, Extraction started for: {youtube_link}, title: {row['Texture Description']}")
            video_id = extract_video_id(youtube_link)
            if not video_id:
                transcript_text = "Invalid YouTube URL"
                summary = ""
            else:
                transcript_text = get_transcript(youtube_link, video_id)
                summary = get_summary(transcript_text)
            row["Transcript"] = transcript_text
            row["Summary"] = summary
            writer.writerow(row)
            # Flush the row immediately so work isn't lost on error.
            outfile.flush()
            os.fsync(outfile.fileno())
            count += 1
    print(f"Processing complete. Updated CSV saved as {output_csv}")

if __name__ == "__main__":
    main()