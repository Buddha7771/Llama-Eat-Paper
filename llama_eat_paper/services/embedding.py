import chromadb
import ollama

from tqdm import tqdm

from llama_eat_paper.integrations import NotionClient
from llama_eat_paper.config import settings


def get_embedding(prompt: str) -> list[float]:
    response = ollama.embeddings(model=settings.EMBEDDING_MODEL, prompt=prompt)
    return response.embedding


def build_collection_from_notion() -> chromadb.Collection:
    client = chromadb.EphemeralClient()
    collection = client.get_or_create_collection(
        name="llama-eat_paper",
        metadata={"hnsw:space": "cosine"},
    )

    notion_client = NotionClient(token=settings.NOTION_TOKEN)
    results = notion_client.fetch_database(settings.NOTION_DATABASE_ID)
    for result in tqdm(results, desc="Building collection from Notion"):
        properties = result["properties"]
        title = properties["title"]["title"]
        abstract = properties["abstract"]["rich_text"]
        url = properties["URL"]["url"]
        if len(title) == 0 or len(abstract) == 0:
            continue
        collection.add(
            ids=title[0]["text"]["content"],
            embeddings=get_embedding(abstract[0]["text"]["content"]),
            documents=url,
        )

    return collection
