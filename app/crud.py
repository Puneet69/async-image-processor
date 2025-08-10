from app.database import jobs_collection
from datetime import datetime
import uuid

async def create_job(job_data: dict) -> dict:
    job_data["request_id"] = str(uuid.uuid4())
    job_data["status"] = "PENDING"
    job_data["created_at"] = datetime.utcnow()
    job_data["completed_at"] = None
    result = await jobs_collection.insert_one(job_data)
    new_job = await jobs_collection.find_one({"_id": result.inserted_id})
    return new_job

async def get_job_by_request_id(request_id: str) -> dict:
    job = await jobs_collection.find_one({"request_id": request_id})
    return job

async def update_job_status(request_id: str, status: str):
    await jobs_collection.update_one(
        {"request_id": request_id},
        {"$set": {"status": status, "completed_at": datetime.utcnow()}}
    )
