from datetime import datetime
from typing import Generator

from openreview.api import OpenReviewClient as Client

from llama_eat_paper.models import Paper


class OpenReviewClient:
    def __init__(self):
        self.client = Client(baseurl="https://api2.openreview.net")

    def fetch_venues(self, conference: str, year: str) -> list[str]:
        venue_list = []
        for venue in self.client.get_group(id="venues").members:
            if venue.startswith(f"{conference}/{year}"):
                venue_list.append(venue)
        return venue_list

    def yield_invitation_papers(
        self,
        invitation: str,
        skip_rejected: bool = False,
    ) -> Generator[Paper, None, None]:
        N = 0
        while True:
            papers = self.client.get_notes(invitation=invitation, limit=1000, offset=N)
            if len(papers) == 0:
                break
            for paper in papers:
                N += 1
                content = paper.content
                if "Rejected" in content["venueid"]["value"] and skip_rejected:
                    continue
                yield Paper(
                    title=content["title"]["value"],
                    authors=content["authors"]["value"] if "authors" in content else [],
                    subjects=content["keywords"]["value"]
                    if "keywords" in content
                    else [],
                    abstract=content["abstract"]["value"].replace("\n", " ")
                    if "abstract" in content
                    else "",
                    submit=datetime.fromtimestamp(paper.tcdate / 1000),
                    pdf_url="https://openreview.net" + content["pdf"]["value"]
                    if "pdf" in content
                    else None,
                    abs_url=f"https://openreview.net/forum?id={paper.id}",
                    journal=content["venue"]["value"],
                )
