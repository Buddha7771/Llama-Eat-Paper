import requests
from datetime import datetime, timezone
from typing import Generator, Optional
from api.info import PaperInfo


def fetch_paper(start_date: datetime,
                end_date: Optional[datetime] = None,
                max_results: int = 100) -> Generator[PaperInfo, None, None]:
    if end_date is None:
        end_date = datetime.now(timezone.utc)
    start_date = start_date.strftime("%Y-%m-%d")
    end_date = end_date.strftime("%Y-%m-%d")

    if max_results > 100:
        max_results = 100
    url = f"https://api.biorxiv.org/details/biorxiv/{start_date}/{end_date}/{max_results}"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()

    for paper in data['collection']:
        url = 'https://www.biorxiv.org/content/' + paper['doi']
        yield PaperInfo(title=paper['title'],
                        authors=paper['authors'].split('; '),
                        subjects=[paper['category']],
                        abstract=paper['abstract'],
                        submit=datetime.strptime(paper['date'], "%Y-%m-%d"),
                        pdf_url=url + '.full.pdf',
                        abs_url=url,
                        journal='bioRxiv')