from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .service import ChooseDocsVariant


class GenerateDocumentView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data

        doc_type = data.get("doc_type")
        if not doc_type:
            return Response({"error": "Поле doc_type обязательно"}, status=status.HTTP_400_BAD_REQUEST)

        generator = ChooseDocsVariant(data)
        try:
            response = generator.worker_method()
            return response  # Возвращаем файл
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Ошибка при генерации документа: {e}")
            return Response({"error": "Произошла ошибка при генерации документа"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
