import os
import numpy as np
import logging
import chromadb
import ollama

from datetime import datetime, timezone, timedelta
from tqdm import tqdm
from dotenv import load_dotenv

from api.info import PaperInfo, JournalIconUrl
from api import arxiv, bioarxiv, slack, notion


def get_embedding(text, model: str = 'mxbai-embed-large'):
    response = ollama.embeddings(model=model, prompt=text)
    return response['embedding']


def main(args):
    logging.basicConfig(format='%(asctime)s - %(levelname)s | %(message)s',
                        # filemode='w',
                        filename='run.log',
                        level=logging.INFO)
    logging.info('loading environment variables')
    load_dotenv()

    logging.info('fetching data from notion')
    database_id = os.getenv('DATABASE_ID')
    notion_token = os.getenv('NOTION_TOKEN')
    data = notion.fetch_database(database_id, notion_token)

    logging.info('creating collection')
    client = chromadb.EphemeralClient()
    collection = client.create_collection(name='ollama-paper-bot',
                                        metadata={"hnsw:space": "cosine"})
    embed_model = args.embedding_model
    for result in data['results']:
        properties = result['properties']
        title = properties['title']['title']
        abstract = properties['abstract']['rich_text']
        url = properties['URL']['url']
        if len(title) == 0 or len(abstract) == 0:
            continue
        embedding = get_embedding(abstract[0]['text']['content'], embed_model)
        collection.add(ids=title[0]['text']['content'],
                       embeddings=embedding,
                       documents=url)

    query_embeddings = []
    query_infos = []
    
    start_date = args.start_date
    if start_date is None:
        start_date = datetime.now(timezone.utc) - timedelta(days=1)
    end_date = args.end_date
    if end_date is None:
        end_date = datetime.now(timezone.utc) - timedelta(days=1)
    logging.info(f'start_date: {start_date}, end_date: {end_date}')
    
    logging.info(f'fetching data from arxiv')
    # because of arxiv new paper announced daily at 01:00 AM UTC,
    # we need to fetch data from 1 days ago
    arxiv_start_date = start_date - timedelta(days=1)
    for paperinfo in tqdm(arxiv.fetch_paper(arxiv_start_date, end_date, max_results=None),
                          desc=f'fetching data from arxiv: {arxiv_start_date} ~ {end_date}'):
        query = f'Represent this abstract for searching relevant abstract:: {paperinfo.abstract}'
        embedding = get_embedding(query, embed_model)
        query_embeddings.append(embedding)
        query_infos.append(paperinfo)

    logging.info('fetching data from bioarxiv')
    for paperinfo in tqdm(bioarxiv.fetch_paper(start_date, end_date),
                          desc=f'fetching data from bioarxiv: {start_date} ~ {end_date}'):
        embedding = get_embedding(paperinfo.abstract, embed_model)
        query_embeddings.append(embedding)
        query_infos.append(paperinfo)

    if len(query_embeddings) == 0:
        logging.info('No new papers to query.')
        return

    results = collection.query(query_embeddings, n_results=3)
    cosine_similarty = 1 - np.array(results['distances'])
    query_idxs = np.where((cosine_similarty > args.threshold).any(-1))[0]

    slack_token = os.getenv('SLACK_TOKEN')
    channel_id = os.getenv('CHANNEL_ID')
    client = slack.SlackAPI(slack_token)

    if len(query_idxs) == 0:
        logging.info('No match papers to query.')
        return

    attachment_list = []
    for query_idx in query_idxs:
        query_info: PaperInfo = query_infos[query_idx]
        if query_info.journal == 'arXiv':
            icon_url = JournalIconUrl.arXiv.value
        elif query_info.journal == 'bioRxiv':
            icon_url = JournalIconUrl.bioRxiv.value
        else:
            icon_url = None

        attachment = {
                    "fallback": "Error",
                    "mrkdwn_in": ["text"],
                    "color": "#454545",
                    "author_name": query_info.journal,
                    "author_link": query_info.abs_url,
                    "author_icon": icon_url,
                    "title": query_info.title,
                    "title_link": query_info.pdf_url,
                    "text": query_info.abstract,
                    "fields": [],
                    "footer": query_info.journal,
                    "footer_icon": icon_url,
                    "ts": query_info.submit.timestamp()
                }
        
        attachment['fields'].append({
            "title": "Authors",
            "value": ', '.join(query_info.authors),
            "short": False
        })
        for i, key_idx in enumerate(np.where(cosine_similarty[query_idx] > args.threshold)[0]):
            url = results['documents'][query_idx][key_idx]
            title = results['ids'][query_idx][key_idx]
            if url is None:
                value = title
            else:
                value = f"<{url}|{title}>"
            attachment['fields'].append({
                "title": f"Top {i+1} related paper (similarity: {cosine_similarty[query_idx][key_idx]:.2f})",
                "value": value,
                "short": False
            })
        attachment_list.append(attachment)
        logging.info(f'Posting message to slack: {query_info.title}')

    text = f"Llama found {len(query_idxs)} papers"
    client.post_message(channel_id=channel_id, text=text, attachments=attachment_list)


if __name__ == '__main__':
    import argparse
    convert_to_datetime = lambda date: datetime.strptime(date, '%Y-%m-%d')
    parser = argparse.ArgumentParser(description='oLlama paper bot arguments.')
    parser.add_argument('--start_date', type=convert_to_datetime, default=None,
                        help='Start date for fetching papers. (e.g. 2025-01-01)')
    parser.add_argument('--end_date', type=convert_to_datetime, default=None,
                        help='End date for fetching papers. (e.g. 2025-01-01)')
    parser.add_argument('--embedding_model', type=str, default='mxbai-embed-large')
    parser.add_argument('--threshold', type=float, default=0.8)
    args = parser.parse_args()
    main(args)
