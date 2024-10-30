from celery import shared_task
from .models import TrackNumber
from .service import TrackService
import logging
from .api_client import TrackNumberAPIView

logger = logging.getLogger(__name__)


@shared_task
def update_info_for_tracks():
    track_numbers = TrackNumber.objects.exclude(
        status__in=["Вручение адресату", "Получено адресатом", "Адресату почтальоном"]
    )

    for track_number_obj in track_numbers:
        track_number = track_number_obj.track
        service = TrackService(track_number)

        result = service.process_tracking()

        if result["status"] == "success":
            if result["new_status"] != result["existing_status"]:
                logger.info(
                    f"Трек-номер {track_number}: статус изменился с {result['existing_status']} на {result['new_status']}"
                )

                create_amo_task.apply_async(
                    (track_number, result["new_status"]), countdown=30
                )
            track_number_obj.status = result["new_status"]
            track_number_obj.save()
        else:
            logger.info(f"Трек-номер {track_number}: статус не изменился")


@shared_task
def create_amo_task(track_number, new_status):

    bebraboi = TrackNumberAPIView()
    bebraboi.create_amo_task(track_number, new_status)
