import arxiv
import logging

from datetime import datetime, timezone
from typing import Generator

from llama_eat_paper.models import Paper

logger = logging.getLogger(__name__)


class ArxivClient:
    def __init__(self, page_size: int = 1000):
        self.client = arxiv.Client(page_size=page_size)

    def yield_papers(
        self,
        start_date: datetime,
        end_date: datetime | None = None,
        max_results: int = 1000,
    ) -> Generator[Paper, None, None]:
        if end_date is None:
            end_date = datetime.now(timezone.utc)
        start_date = start_date.replace(hour=0, minute=0, second=0).strftime(
            "%Y%m%d%H%M"
        )
        end_date = end_date.replace(hour=23, minute=59, second=59).strftime(
            "%Y%m%d%H%M"
        )

        search = arxiv.Search(
            max_results=max_results,
            query=f"submittedDate:[{start_date} TO {end_date}]",
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        try:
            for result in self.client.results(search):
                yield Paper(
                    title=result.title,
                    authors=[author.name for author in result.authors],
                    subjects=result.categories,
                    abstract=result.summary.replace("\n", " "),
                    submit=result.published,
                    pdf_url=result.pdf_url,
                    abs_url=result.entry_id,
                    journal="arXiv",
                )
        except Exception as e:
            logger.error(f"Error fetching papers from arXiv: {e}")
            return
