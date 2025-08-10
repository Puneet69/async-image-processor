from fastapi import FastAPI, UploadFile, Form, HTTPException, BackgroundTasks, Path
from fastapi.responses import FileResponse
import pandas as pd
from io import StringIO
import os

from app.crud import create_job, get_job_by_request_id
from app.workers import process_images
from app.csv_utils import save_results_csv  # import only

app = FastAPI()

CSV_DIR = "./processed_results"
os.makedirs(CSV_DIR, exist_ok=True)


@app.get("/")
async def root():
    return {"message": "Async Image Processor API is running!"}


@app.post("/upload")
async def upload_csv(
    file: UploadFile,
    webhook_url: str = Form(None),
    background_tasks: BackgroundTasks = None,
):
    content = await file.read()
    csv_str = content.decode("utf-8")
    df = pd.read_csv(StringIO(csv_str))

    required_columns = ["Serial Number", "Product Name", "Input Image Urls"]
    if not all(col in df.columns for col in required_columns):
        raise HTTPException(status_code=400, detail="CSV missing required columns")

    images_list = []
    for _, row in df.iterrows():
        urls = [url.strip() for url in row["Input Image Urls"].split(",")]
        for url in urls:
            images_list.append(
                {
                    "serial_number": int(row["Serial Number"]),
                    "product_name": row["Product Name"],
                    "original_url": url,
                    "status": "PENDING",
                }
            )

    job_data = {
        "webhook_url": webhook_url,
        "images": images_list,
    }

    job = await create_job(job_data)

    if background_tasks:
        background_tasks.add_task(process_images, job["request_id"], webhook_url)

    return {"request_id": job["request_id"], "status": "PENDING"}


@app.get("/status/{request_id}")
async def get_status(request_id: str):
    job = await get_job_by_request_id(request_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return {"request_id": job["request_id"], "status": job["status"]}


@app.get("/download/{request_id}")
async def download_csv(request_id: str = Path(..., description="Job request ID")):
    csv_path = os.path.join(CSV_DIR, f"{request_id}.csv")
    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")
    return FileResponse(csv_path, media_type="text/csv", filename=f"results_{request_id}.csv")
