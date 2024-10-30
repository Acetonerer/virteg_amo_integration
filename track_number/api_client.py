from rest_framework.views import APIView
from rest_framework.response import Response
from .service import TrackService
from .amo_client import AmoClientApi
from .models import TrackNumber
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logger = logging.getLogger(__name__)


class TrackNumberAPIView(APIView):

    def get(self, request, track_number):
        service = TrackService(track_number)

        result = service.process_tracking()

        if result.get("status") == "success":
            if result.get("new_status") is not None and result.get(
                "new_status"
            ) != result.get("existing_status"):
                new_status = result.get("new_status")
                self.create_amo_task(track_number, new_status)
            else:
                logger.info("Статус не изменился, задача не будет создана.")
        else:
            pass
            # logger.error("Ошибка в процессе отслеживания: " + result.get("error", "неизвестная ошибка"))

        return Response(result)

    def create_amo_task(self, track_number, new_status):
        """Создание задачи в AmoCRM с текстом, содержащим информацию о статусе."""
        AMO_DOMAIN = os.environ.get("AMO_DOMAIN")
        AMO_DEAL_ID = os.environ.get("AMO_DEAL_ID")
        AMO_TOKEN = os.environ.get("AMO_TOKEN")

        try:
            existing_record = TrackNumber.objects.get(track=track_number)
            sender_name = existing_record.name_sender
        except TrackNumber.DoesNotExist:
            logger.error(f"Запись с трек-номером {track_number} не найдена.")
            return

        amo_client = AmoClientApi(
            access_token=AMO_TOKEN,
            amocrm_domain=AMO_DOMAIN,
            amo_deal_id=int(AMO_DEAL_ID),
        )

        task_text = f'Для почтового отправления от {sender_name} с номером №{track_number} статус изменился на "{new_status}"'
        response = amo_client.send_request_for_amo_task(text=task_text)

        if response.get("_embedded") and response["_embedded"].get("tasks"):
            task_id = response["_embedded"]["tasks"][0]["id"]
            logger.info(f"Задача успешно создана в AmoCRM с ID: {task_id}")
        else:
            logger.error(f"Ошибка при создании задачи в AmoCRM: {response}")

        return response
