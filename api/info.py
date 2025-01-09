from datetime import datetime
from enum import Enum
from dataclasses import dataclass

@dataclass
class PaperInfo:
    title: str
    authors: list[str]
    subjects: list[str]
    abstract: str
    submit: datetime
    pdf_url: str
    abs_url: str
    journal: str = None


class JournalIconUrl(Enum):
    arXiv = 'https://ca.slack-edge.com/T04H68QRY5N-U087GQBCUS1-44b4a82a59e6-512'
    bioRxiv = 'https://ca.slack-edge.com/T04H68QRY5N-U087GQBCUS1-44b4a82a59e6-512'
