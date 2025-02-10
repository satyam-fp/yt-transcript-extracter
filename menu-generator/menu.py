import os
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from openai import OpenAI

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key as an environment variable
openai_api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Mount static directory to serve JS, CSS, and other static files.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Allow all CORS origins so the JS can call our endpoints.

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def read_index(request: Request):
    """Serve the main UI page."""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-menu")
async def generate_menu(request: Request):
    """
    Generate a North Indian food menu given the list of fridge items.
    Calls the ChatGPT API to generate 3 - 5 dish names and descriptions.
    """
    data = await request.json()
    items = data.get("items", [])
    if not items:
        return JSONResponse(content={"error": "No items provided."}, status_code=400)

    # Construct prompt for ChatGPT
    prompt = (
        "You are a chef specialized in North Indian cuisine. "
        "Given the following available ingredients in a fridge: " + ", ".join(items) + ". "
        "Please suggest a North Indian food menu that can be cooked using these ingredients. "
        "Provide 3 to 5 dish names along with a brief description for each dish. "
        "Format your answer in a markdown list."
        "Do not include any food item that cannot be cooked using the ingredients provided."
    )

    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[


                {"role": "system", "content": "You are a creative and helpful assistant."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.7,
        )
        menu_text = response.choices[0].message.content.strip()
        return {"menu": menu_text}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


@app.post("/process-voice")
async def process_voice(request: Request):
    """
    Process transcribed voice text to extract a list of items.
    Calls ChatGPT to extract and return a clean, comma-separated list of ingredients.
    """
    data = await request.json()
    voice_text = data.get("voice_text", "")
    if not voice_text:
        return JSONResponse(content={"error": "No voice text provided."}, status_code=400)

    prompt = (
        "Extract a list of fridge items from the following text. "
        "Return the result as a comma separated list without any extra description.\n\n"
        f"Text: {voice_text}"
    )

    try:
        client = OpenAI(api_key=openai_api_key)
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You extract information from text."},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )
        result_text = response.choices[0].message.content.strip()
        # Clean and split the extracted text into a list.
        items_list = [item.strip() for item in result_text.split(",") if item.strip()]
        return {"items": items_list}
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)


if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
