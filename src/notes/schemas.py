from datetime import datetime

from pydantic import BaseModel, Field


class Note(BaseModel):
    user_id: int
    note_id: int
    note_title: str = Field(min_length=1, max_length=30)
    note_text: str = Field(min_length=1, max_length=500)
