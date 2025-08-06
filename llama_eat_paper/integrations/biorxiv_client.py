import requests
import logging

from datetime import datetime, timezone
from typing import Generator

from llama_eat_paper.models import Paper


logger = logging.getLogger(__name__)


class BioRxivClient:
    api_url = "https://api.biorxiv.org/details/biorxiv"
    content_url = "https://www.biorxiv.org/content"

    def __init__(self):
        pass

    def _fetch_papers(
        self,
        start_date: str,
        end_date: str,
        cursor: int,
    ) -> list[dict]:
        url = f"{self.api_url}/{start_date}/{end_date}/{cursor}"
        response = requests.get(url)
        response.raise_for_status()

        data = response.json()
        return data["collection"]

    def yield_papers(
        self,
        start_date: datetime,
        end_date: datetime | None = None,
    ) -> Generator[Paper, None, None]:
        if end_date is None:
            end_date = datetime.now(timezone.utc)
        start_date = start_date.strftime("%Y-%m-%d")
        end_date = end_date.strftime("%Y-%m-%d")

        cursor = 0

        while True:
            try:
                papers = self._fetch_papers(start_date, end_date, cursor)
            except requests.RequestException as e:
                logger.error(f"Error fetching papers from bioRxiv: {e}")
                return

            if len(papers) == 0:
                break
            cursor += 100

            for paper in papers:
                url = f"{self.content_url}/{paper['doi']}"
                yield Paper(
                    title=paper["title"],
                    authors=paper["authors"].split("; "),
                    subjects=[paper["category"]],
                    abstract=paper["abstract"],
                    submit=datetime.strptime(paper["date"], "%Y-%m-%d"),
                    pdf_url=url + ".full.pdf",
                    abs_url=url,
                    journal="bioRxiv",
                )
