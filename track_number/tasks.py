from celery import shared_task
from .models import TrackNumber
from .service import TrackService
import logging
from .api_client import TrackNumberAPIView

logger = logging.getLogger(__name__)


@shared_task
def update_info_for_tracks():
    track_numbers = TrackNumber.objects.all()
    for track_number_obj in track_numbers:
        track_number = track_number_obj.track
        service = TrackService(track_number)

        result = service.process_tracking()

        if result["status"] == "success" and result["new_status"] != result["existing_status"]:
            logger.info(
                f"Трек-номер {track_number}: статус изменился с {result['existing_status']} на {result['new_status']}")
            bebraboi = TrackNumberAPIView()
            bebraboi.create_amo_task(track_number, result['new_status'])
            return "У нас новый крутой статус!"
        else:
            logger.info(f"Трек-номер {track_number}: статус не изменился")
            return "У нас старый, но тоже крутой статус!"
