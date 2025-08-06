from datetime import datetime
from pydantic import BaseModel


class Paper(BaseModel):
    title: str
    abstract: str
    submit: datetime
    abs_url: str
    subjects: list[str] | None = None
    authors: list[str] | None = None
    pdf_url: str | None = None
    journal: str | None = None
