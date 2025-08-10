from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import datetime

class ImageModel(BaseModel):
    serial_number: int
    product_name: str
    original_url: HttpUrl
    processed_url: Optional[HttpUrl] = None
    status: str = "PENDING"

class JobModel(BaseModel):
    request_id: UUID = Field(default_factory=uuid4)
    status: str = "PENDING"
    webhook_url: Optional[HttpUrl] = None  # Changed to HttpUrl for validation
    images: List[ImageModel] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
