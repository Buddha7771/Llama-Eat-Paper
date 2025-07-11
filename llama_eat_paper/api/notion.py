import requests


def fetch_database(databaseId: str,
                   notion_token: str) -> dict:
    url = f"https://api.notion.com/v1/databases/{databaseId}/query"
    headers = {"Authorization": "Bearer " + notion_token,
               "Notion-Version": "2022-02-22"}

    response = requests.post(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    return data
