from datetime import datetime
from pydantic import BaseModel, ConfigDict

class FileInfo(BaseModel):
    id: int
    original_name: str
    ext: str
    size: int
    content_type: str | None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)