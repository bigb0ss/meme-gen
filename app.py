from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from openai import OpenAI
import uvicorn
from dotenv import load_dotenv
import os
from PIL import Image, ImageDraw, ImageFont
from fastapi.responses import StreamingResponse
import shutil
import io

import uvicorn
load_dotenv()

app = FastAPI()


@app.post("/meme/image/")
async def upload_image(file: UploadFile = File(...)):
    os.makedirs("images/", exist_ok=True)
    file_location = f"images/{file.filename}"
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    return {"filename": file.filename}

@app.get("/meme/image/")
async def get_image(filename: str):
    file_location = f"images/{filename}"
    return FileResponse(file_location)

@app.get("/meme/images")
async def get_images():
    images = os.listdir("images")
    return {"images": images}

@app.get("/meme/generate")
async def generate_meme(image:str, text:str, y:int):

    # Draw top and bottom text
    image = Image.open(f"images/{image}").convert("RGB")
    draw = ImageDraw.Draw(image)
    font = ImageFont.load_default()
    font.size = 80

    text = text.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Center text
    x = (image.width - text_width) // 2
    y = (image.height - text_height) // 2
    # x = (width - text_width) / 2
    draw.text((x, y), text, font=font, fill="black", stroke_width=10, stroke_fill="white")


    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    buf.seek(0)

    return StreamingResponse(buf, media_type="image/jpeg")



if __name__ == "__main__":
    uvicorn.run(app, port=8000)