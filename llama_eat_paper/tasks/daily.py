import datetime
import logging
import numpy as np

from llama_eat_paper.integrations import ArxivClient, BioRxivClient
from llama_eat_paper.services.embedding import (
    get_embedding,
    build_collection_from_notion,
)
from llama_eat_paper.services.slack_messenger import (
    SimilarityResult,
    MatchedPaper,
    send_matched_papers_to_slack,
)

logger = logging.getLogger(__name__)


def run_daily_task(
    start_date: datetime.date,
    end_date: datetime.date,
    threshold: float = 0.8,
    n_results: int = 3,
):
    collection = build_collection_from_notion()
    query_embeddings = []
    query_papers = []
    prompt = "Represent this abstract for searching relevant abstract: "

    arxiv_client = ArxivClient()
    for papar in arxiv_client.yield_papers(start_date, end_date):
        embedding = get_embedding(prompt + papar.abstract)
        query_embeddings.append(embedding)
        query_papers.append(papar)

    biorxiv_client = BioRxivClient()
    for papar in biorxiv_client.yield_papers(start_date, end_date):
        embedding = get_embedding(prompt + papar.abstract)
        query_embeddings.append(embedding)
        query_papers.append(papar)

    if not query_embeddings:
        logger.info("No new papers to query.")
        return

    query_results = collection.query(query_embeddings, n_results=n_results)
    query_similarity = 1 - np.array(query_results["distances"])

    matched_papers = []
    for query_idx, query_paper in enumerate(query_papers):
        results = []
        for key_idx, similarity in enumerate(query_similarity[query_idx]):
            if similarity > threshold:
                result = SimilarityResult(
                    title=query_results["ids"][query_idx][key_idx],
                    url=query_results["documents"][query_idx][key_idx],
                    similarity=similarity,
                )
                results.append(result)
        if results:
            matched_paper = MatchedPaper(
                query_paper=query_paper,
                results=results,
            )
            matched_papers.append(matched_paper)

    if not matched_papers:
        logging.info("No matched papers found.")
        return

    send_matched_papers_to_slack(matched_papers)
