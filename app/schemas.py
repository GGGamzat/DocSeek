from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List


class DocumentResponse(BaseModel):
    id: int
    text: str
    created_date: datetime
    rubrics: List[str]

    model_config = ConfigDict(from_attributes=True)