from pydantic import BaseModel
from slack_sdk import WebClient

from llama_eat_paper.schemas import Paper, JournalIconUrl
from llama_eat_paper.config import settings


class SimilarityResult(BaseModel):
    title: str
    url: str | None = None
    similarity: float


class MatchedPaper(BaseModel):
    query_paper: Paper
    results: list[SimilarityResult]


def _build_attachment(matched: MatchedPaper) -> dict:
    if matched.query_paper.journal == "arXiv":
        icon_url = JournalIconUrl.arXiv.value
    elif matched.query_paper.journal == "bioRxiv":
        icon_url = JournalIconUrl.bioRxiv.value
    elif matched.query_paper.journal.startswith("ICLR"):
        icon_url = JournalIconUrl.ICLR.value
    elif matched.query_paper.journal.startswith("ICML"):
        icon_url = JournalIconUrl.ICML.value
    elif matched.query_paper.journal.startswith("NeurIPS"):
        icon_url = JournalIconUrl.NeurIPS.value
    else:
        icon_url = None

    attachment = {
        "fallback": "Error",
        "mrkdwn_in": ["text"],
        "color": "#454545",
        "author_name": matched.query_paper.journal,
        "author_link": matched.query_paper.abs_url,
        "author_icon": icon_url,
        "title": matched.query_paper.title,
        "title_link": matched.query_paper.pdf_url,
        "text": matched.query_paper.abstract,
        "fields": [],
        "footer": matched.query_paper.journal,
        "footer_icon": icon_url,
        "ts": matched.query_paper.submit.timestamp(),
    }

    if matched.query_paper.authors:
        authors = ", ".join(matched.query_paper.authors)
    else:
        authors = "Unknown Authors"
    attachment["fields"].append(
        {
            "title": "Authors",
            "value": authors,
            "short": False,
        }
    )

    for i, result in enumerate(matched.results):
        if result.url is None:
            value = result.title
        else:
            value = f"<{result.url}|{result.title}>"
        attachment["fields"].append(
            {
                "title": f"Top {i + 1} related paper (similarity: {result.similarity:.3f})",
                "value": value,
                "short": False,
            }
        )
    return attachment


def send_matched_papers_to_slack(matched_papers: list[MatchedPaper]) -> None:
    attachment_list = []
    for matched in matched_papers:
        attachment = _build_attachment(matched)
        attachment_list.append(attachment)

    client = WebClient(token=settings.SLACK_TOKEN)
    response = client.chat_postMessage(
        channel=settings.SLACK_CHANNEL_ID,
        text=f"Llama found {len(matched_papers)} papers",
    )
    for attachment in attachment_list:
        client.chat_postMessage(
            channel=settings.SLACK_CHANNEL_ID,
            thread_ts=response["ts"],
            attachments=[attachment],
        )
