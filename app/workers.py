import asyncio
from app.database import jobs_collection
from app.utils import download_image, compress_image, save_image_locally
from datetime import datetime
import httpx
from app.csv_utils import save_results_csv

async def process_images(request_id: str, webhook_url: str = None):
    job = await jobs_collection.find_one({"request_id": request_id})
    if not job:
        print(f"No job found with request_id: {request_id}")
        return
    
    images = job.get("images", [])
    
    semaphore = asyncio.Semaphore(5)  # Limit concurrency to 5

    async def process_single(image):
        async with semaphore:
            try:
                original_url = image["original_url"]
                image_bytes = await download_image(original_url)
                compressed_bytes = compress_image(image_bytes, quality=50)
                saved_path = save_image_locally(compressed_bytes)

                image["processed_url"] = saved_path
                image["status"] = "COMPLETED"
            except Exception as e:
                image["status"] = "FAILED"
                print(f"Error processing image {image.get('original_url')}: {e}")

    # Process all images concurrently (up to 5 at a time)
    await asyncio.gather(*(process_single(img) for img in images))

    # Update job document with new image statuses and completion time
    await jobs_collection.update_one(
        {"request_id": request_id},
        {
            "$set": {
                "status": "COMPLETED",
                "completed_at": datetime.utcnow(),
                "images": images
            }
        }
    )

    # Fetch updated job to save CSV with the latest data
    updated_job = await jobs_collection.find_one({"request_id": request_id})

    # Save results CSV locally
    await save_results_csv(updated_job)

    # If webhook_url provided, notify the endpoint asynchronously
    if webhook_url:
        async with httpx.AsyncClient() as client:
            try:
                await client.post(webhook_url, json={"request_id": request_id, "status": "COMPLETED"})
            except Exception as e:
                print(f"Error triggering webhook: {e}")
