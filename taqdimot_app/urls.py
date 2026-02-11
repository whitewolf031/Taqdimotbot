from django.urls import path
from taqdimot_app.api.views import generate_work
from taqdimot_app.views import GenerateSlideAPIView

urlpatterns = [
    path("generate-work/", generate_work, name="generate-work"),
    path("generate-slide/", GenerateSlideAPIView().as_view())
]
