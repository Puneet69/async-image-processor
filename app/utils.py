import os
from io import BytesIO
from PIL import Image
import httpx
import uuid

# Folder to save compressed images locally
OUTPUT_FOLDER = "processed_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

async def download_image(url: str) -> BytesIO:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return BytesIO(response.content)

def compress_image(image_bytes: BytesIO, quality: int = 50) -> BytesIO:
    image = Image.open(image_bytes)
    compressed_io = BytesIO()
    if image.mode in ("RGBA", "LA") or (image.mode == "P" and "transparency" in image.info):
        # Convert PNG with transparency to RGB with white background
        background = Image.new("RGB", image.size, (255, 255, 255))
        background.paste(image, mask=image.split()[-1])  # alpha channel
        background.save(compressed_io, format="JPEG", quality=quality)
    else:
        image.save(compressed_io, format="JPEG", quality=quality)
    compressed_io.seek(0)
    return compressed_io

def save_image_locally(image_bytes: BytesIO) -> str:
    filename = f"{uuid.uuid4()}.jpg"
    filepath = os.path.join(OUTPUT_FOLDER, filename)
    with open(filepath, "wb") as f:
        f.write(image_bytes.read())
    # Return URL path assuming OUTPUT_FOLDER is served statically
    return f"/{OUTPUT_FOLDER}/{filename}"
