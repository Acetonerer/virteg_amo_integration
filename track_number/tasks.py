from celery import shared_task
from .models import TrackNumber
from .service import TrackService
import logging
from .api_client import TrackNumberAPIView

logger = logging.getLogger(__name__)


@shared_task
def update_info_for_tracks():
    logger.info("Запуск задачи update_info_for_tracks")
    track_numbers = TrackNumber.objects.all()
    logger.info(f"Найдено {track_numbers.count()} трек-номеров для обработки")

    for track_number_obj in track_numbers:
        track_number = track_number_obj.track
        logger.info(f"Обработка трек-номера: {track_number}")

        try:
            service = TrackService(track_number)
            result = service.process_tracking()
            logger.info(f"Результат для трек-номера {track_number}: {result}")
        except Exception as e:
            logger.error(f"Ошибка при обработке трек-номера {track_number}: {e}")
            continue

        if result["status"] == "success" and result["new_status"] != result["existing_status"]:
            try:
                logger.info(f"Статус изменился, создание задачи для AmoCRM для трек-номера {track_number}")
                bebraboi = TrackNumberAPIView()
                bebraboi.create_amo_task(track_number, result['new_status'])
                logger.info(f"Задача для AmoCRM успешно создана для трек-номера {track_number}")
            except Exception as e:
                logger.error(f"Ошибка при создании задачи для AmoCRM: {e}")
        else:
            logger.info(f"Статус для трек-номера {track_number} не изменился")
