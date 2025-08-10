# Async Image Processor API

An asynchronous image processing service built with FastAPI that accepts CSV uploads containing image URLs, processes images by downloading and compressing them, and returns results with status tracking and downloadable CSV reports.

---

## Features

- Upload CSV with product image URLs.
- Asynchronously download and compress images.
- Track processing status by request ID.
- Webhook support for job completion notifications.
- Download processed results as CSV.
- MongoDB used for data storage.

---

## Tech Stack

- Python 3.13+
- FastAPI (Web API)
- Uvicorn (ASGI server)
- MongoDB (Database)
- httpx (Async HTTP client)
- Pillow (Image processing)
- Pandas (CSV reading)
- Pydantic (Data validation)

---

## Prerequisites

- Python 3.13 or above installed
- MongoDB server running locally or remotely
- Git installed
- (Optional) Virtual environment tool (venv, virtualenv)

---

## Setup Instructions

1. Clone the repository

``git clone https://github.com/Puneet69/async-image-processor.git
cd async-image-processor``

---

2. Create and activate a Python virtual environment
  ``python3 -m venv venv
source venv/bin/activate      # On Windows: venv\Scripts\activate``

---

4. Install dependencies
``pip install -r requirements.txt``

---

6. Configure MongoDB
``mongodb://localhost:27017``

---

8. Run the FastAPI server
``uvicorn app.main:app --reload``

---


10. Post request
  example: ``curl -X POST "http://127.0.0.1:8000/upload" -F "file=@products_images.csv"``

---

API Endpoints

1. Root
GET /
Returns a welcome message confirming API is running.

---

3. Upload CSV
POST /upload
Upload a CSV file containing product images to process asynchronously.
Form fields:
file (CSV file)
webhook_url (optional string URL to receive completion callback)
CSV file must have columns:
"Serial Number", "Product Name", "Input Image Urls" (comma-separated URLs)
Response:
{
  "request_id": "unique-request-id",
  "status": "PENDING"
}

---

4. Check Job Status
GET /status/{request_id}
Get the current status of a job using the request_id.
Response example:
{
  "request_id": "unique-request-id",
  "status": "PENDING | COMPLETED"
}

---


5. Download Results CSV
GET /download/{request_id}
Download the processed results CSV for the given job.
How It Works
Upload a CSV with product image URLs.
The server creates a job and queues image processing asynchronously.
Images are downloaded, compressed, and saved locally.
Job status updates from PENDING to COMPLETED once all images are processed.
Processed data saved as CSV which can be downloaded.
If provided, webhook URL is called on completion.

---

Notes
Ensure your CSV URLs are publicly accessible.
Output images and CSV are saved locally in processed_images and processed_results folders.
Adjust concurrency limits and quality settings in workers/utils as needed.
Testing the API
You can test the API easily using tools like Postman or [curl].

---

Example curl to upload CSV:

curl -X POST "http://127.0.0.1:8000/upload" -F "file=@yourfile.csv" -F "webhook_url=https://your-webhook.url"
License
MIT License
Author
Puneet Gupta
GitHub Profile
