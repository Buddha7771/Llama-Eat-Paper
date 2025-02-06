import openreview

from datetime import datetime
from typing import Generator

from api.info import PaperInfo


def fetch_venues(
        conference: str,
        year: str
    ) -> list[str]:
    client = openreview.api.OpenReviewClient(
        baseurl='https://api2.openreview.net',
    )
    venue_list = []
    for venue in client.get_group(id='venues').members:
        if venue.startswith(f'{conference}/{year}'):
            venue_list.append(venue)
    return venue_list


def fetch_invitation_paper(
        invitation: str,
        skip_rejected: bool = False
    ) -> Generator[PaperInfo, None, None]:
    client = openreview.api.OpenReviewClient(
        baseurl='https://api2.openreview.net'
    )
    N = 0
    while True:
        papers = client.get_notes(
            invitation=invitation,
            limit=1000,
            offset=N
        )
        if len(papers) == 0:
            break
        for paper in papers:
            N += 1
            content = paper.content
            if 'Rejected' in content['venueid']['value'] and skip_rejected:
                continue
            yield PaperInfo(
                title=content['title']['value'],
                authors=content['authors']['value'] if 'authors' in content else [],
                subjects=content['keywords']['value'] if 'keywords' in content else [],
                abstract=content['abstract']['value'].replace('\n', ' '),
                submit=datetime.fromtimestamp(paper.tcdate / 1000),
                pdf_url="https://openreview.net" + content["pdf"]['value'] if "pdf" in content else None,
                abs_url=f"https://openreview.net/forum?id={paper.id}",
                journal=content['venue']['value'],
            )
