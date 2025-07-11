from typing import Optional
from datetime import datetime
from enum import Enum
from dataclasses import dataclass

@dataclass
class PaperInfo:
    title: str
    abstract: str
    submit: datetime
    abs_url: str
    subjects: Optional[list[str]] = None
    authors: Optional[list[str]] = None
    pdf_url: Optional[str] = None
    journal: Optional[str] = None


class JournalIconUrl(Enum):
    arXiv = 'https://ca.slack-edge.com/T04H68QRY5N-U087GQBCUS1-44b4a82a59e6-512'
    bioRxiv = 'https://ca.slack-edge.com/T04H68QRY5N-U087GQBCUS1-44b4a82a59e6-512'
    ICLR = 'https://pbs.twimg.com/profile_images/1242741510929612801/Mt1ozX07_400x400.jpg'
    ICML = 'https://pbs.twimg.com/profile_images/1264614967908552704/ea0u5NgU_400x400.jpg'
    NeurIPS = 'https://pbs.twimg.com/profile_images/1324732596622950401/jmCoOBzX_400x400.jpg'
