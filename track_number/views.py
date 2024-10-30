import logging
import os
from dotenv import load_dotenv
from suds.client import Client

load_dotenv()
logger = logging.getLogger(__name__)


class BaseRussiaMail:

    LOGIN = os.environ.get("RUSSIA_LOGIN")
    PASSWORD = os.environ.get("RUSSIA_PASSWORD")
    RUSSIA_URL = os.environ.get("URL")

    def __init__(self, login=LOGIN, url=RUSSIA_URL, password=PASSWORD):
        self.login = login
        self.password = password
        self.url = url
        self.client = Client(
            self.url, headers={"Content-Type": "application/soap+xml; charset=utf-8"}
        )


class GetTrackNumberFromRussia(BaseRussiaMail):
    """
    Класс для обращения к API Почты России для одиночного трек-номера.
    """

    def get_ticket(self, track_number):
        """
        Метод для получения билета на подготовку информации по трек-номеру (getTicket).
        """
        try:
            # Формируем SOAP-запрос
            message = f"""<?xml version="1.0" encoding="UTF-8"?>
                                <soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope" xmlns:oper="http://russianpost.org/operationhistory" xmlns:data="http://russianpost.org/operationhistory/data" xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/">
                                <soap:Header/>
                                <soap:Body>
                                   <oper:getOperationHistory>
                                      <data:OperationHistoryRequest>
                                         <data:Barcode>{track_number}</data:Barcode>  
                                     <data:MessageType>0</data:MessageType>
                                     
                                  </data:OperationHistoryRequest>
                                  <data:AuthorizationHeader soapenv:mustUnderstand="1">
                                     <data:login>{self.login}</data:login>
                                     <data:password>{self.password}</data:password>
                                  </data:AuthorizationHeader>
                               </oper:getOperationHistory>
                            </soap:Body>
                         </soap:Envelope>"""

            # Отправляем запрос
            result = self.client.service.getOperationHistory(
                __inject={"msg": message.encode("utf-8")}
            )
            history = []
            for rec in result.historyRecord:
                record = {
                    "date": str(rec.OperationParameters.OperDate),
                    "location": rec.AddressParameters.OperationAddress.Description,
                    "status": (
                        rec.OperationParameters.OperAttr.Name
                        if hasattr(rec.OperationParameters.OperAttr, "Name")
                        else "Не указано"
                    ),
                    "sender": rec.UserParameters.Sndr,
                }
                history.append(record)
            return history

        except Exception as error:
            logger.error(f"Error in get_ticket: {error}")
            print(f"Error: {error}")
