from .views import GetTrackNumberFromRussia, BaseRussiaMail
from .models import TrackNumber
import logging
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


class TrackService(BaseRussiaMail):

    def __init__(self, track_number):
        super().__init__(track_number)
        self.track_number = track_number
        self.russia_mail = GetTrackNumberFromRussia()

    def fetch_tracking_data(self):
        """Получает данные по трек-номеру от API Почты России"""
        try:
            tracking_result = self.russia_mail.get_ticket(self.track_number)

            if tracking_result:
                return {"data": tracking_result}
            return {"error": "Unable to retrieve tracking data."}

        except Exception as error:
            logger.error(f"Error in fetch_tracking_data: {error}")
            return {"Error": "Failed to fetch tracking data."}

    def save_check_update_tracking(self, tracking_result):
        """Сохраняет или обновляет данные по трек-номеру в базе данных."""
        logger.debug(f"Tracking result: {tracking_result}")

        if not tracking_result:
            logger.error("Отсутствуют данные для отслеживания.")
            return None

        first_record = tracking_result[0]
        last_record = tracking_result[-1]
        new_status = last_record["status"]
        sender = first_record.get("sender")
        track_number = self.track_number

        if not self._validate_track_number(track_number):
            return None

        existing_record = self._get_existing_record(track_number)

        if existing_record is None:
            logger.info(f"Создание новой записи для трек-номера {track_number}.")
            self._create_new_record(track_number, new_status, sender)
            return new_status

        if existing_record.status != new_status:
            logger.info(
                f"Статус трек-номера {existing_record.track} изменился с '{existing_record.status}' на '{new_status}'."
            )
            existing_record.status = new_status
            existing_record.save()
            return new_status

        logger.info(f"Статус для трек-номера {existing_record.track} не изменился.")
        return None

    @staticmethod
    def _validate_track_number(track_number):
        """Проверка валидности трек-номера"""
        if not track_number:
            logger.error("Трек-номер не получен, пропускаем создание записи.")
            return False
        return True

    @staticmethod
    def _get_existing_record(track_number):
        """Получение существующей записи по трек-номеру"""
        try:
            return TrackNumber.objects.get(track=track_number)
        except TrackNumber.DoesNotExist:
            logger.info(f"Запись для трек-номера {track_number} не найдена.")
            return None

    @staticmethod
    def _create_new_record(track_number, new_status, sender):
        """Создание новой записи для трек-номера"""
        TrackNumber.objects.create(track=track_number, status=new_status, name=sender)

    def process_tracking(self):
        """Метод обработки полученных данных по трек-номеру"""
        tracking_data = self.fetch_tracking_data()
        if "error" in tracking_data:
            logger.error(f"Ошибка при получении данных: {tracking_data['error']}")
            return {"error": tracking_data["error"]}

        existing_record = self._get_existing_record(self.track_number)
        existing_status = existing_record.status if existing_record else None

        new_status = self.save_check_update_tracking(tracking_data["data"])

        return {
            "status": "success" if new_status else "no_update",
            "new_status": new_status,
            "existing_status": existing_status,
        }
