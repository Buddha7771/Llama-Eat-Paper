import requests


class NotionClient:
    database_url = "https://api.notion.com/v1/databases"

    def __init__(self, token: str):
        self.token = token

    @property
    def headers(self) -> dict:
        return {
            "Authorization": "Bearer " + self.token,
            "Notion-Version": "2022-02-22",
        }

    def fetch_database(self, database_id: str) -> dict:
        url = f"{self.database_url}/{database_id}/query"
        response = requests.post(url, headers=self.headers)
        response.raise_for_status()
        data = response.json()
        return data["results"]
