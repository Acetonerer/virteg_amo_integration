from django.urls import path
from .views import GenerateDocumentView

urlpatterns = [
    path('api/generate-document/', GenerateDocumentView.as_view(), name='generate_document'),
]
