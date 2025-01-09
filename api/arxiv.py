import arxiv

from datetime import datetime, timezone
from typing import Generator, Optional

from api.info import PaperInfo


def fetch_paper(start_date: datetime,
                end_date: Optional[datetime] = None,
                max_results: Optional[int] = 1000) -> Generator[PaperInfo, None, None]:
    if end_date is None:
        end_date = datetime.now(timezone.utc)
    start_date = start_date.replace(hour=0, minute=0, second=0).strftime("%Y%m%d%H%M")
    end_date = end_date.replace(hour=23, minute=59, second=59).strftime("%Y%m%d%H%M")

    # arXiv 클라이언트 생성
    client = arxiv.Client(page_size=1000)
    search = arxiv.Search(
        max_results=max_results,
        query=f"submittedDate:[{start_date} TO {end_date}]",  # 제출 날짜 필터,
        sort_by=arxiv.SortCriterion.SubmittedDate,  # 제출 날짜 기준 정렬
        sort_order=arxiv.SortOrder.Descending       # 최신 순 정렬
    )
    for result in client.results(search):
        yield PaperInfo(title=result.title,
                        authors=[author.name for author in result.authors],
                        subjects=result.categories,
                        abstract=result.summary.replace('\n', ' '),
                        submit=result.published,
                        pdf_url=result.pdf_url,
                        abs_url=result.entry_id,
                        journal='arXiv')
