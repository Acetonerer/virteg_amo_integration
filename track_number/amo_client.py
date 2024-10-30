import os
import logging
from dotenv import load_dotenv
import requests
from datetime import datetime

load_dotenv()
logger = logging.getLogger(__name__)


class AmoClientApi:
    """
    Класс для работы с API AmoCRM
    """

    AMO_DOMAIN = os.environ.get("AMO_DOMAIN")
    AMO_DEAL_ID = os.environ.get("AMO_DEAL_ID")
    AMO_TOKEN = os.environ.get("AMO_TOKEN")

    def __init__(
        self,
        access_token=AMO_TOKEN,
        amocrm_domain=AMO_DOMAIN,
        amo_deal_id=AMO_DEAL_ID,
        refresh_token=None,
    ):
        self.access_token = access_token
        self.amocrm_domain = amocrm_domain
        self.amo_deal_id = amo_deal_id
        self.refresh_token = refresh_token

    def send_request_for_amo_task(self, text=""):
        oyea_now = datetime.now()
        current_timestamp = int(oyea_now.timestamp())
        url = f"https://{self.amocrm_domain}/api/v4/tasks"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.access_token}",
        }
        data = [
            {
                "text": text,
                "complete_till": current_timestamp,
                "entity_id": self.amo_deal_id,
                "entity_type": "leads",
            }
        ]

        response = requests.post(url, json=data, headers=headers)
        return response.json()
