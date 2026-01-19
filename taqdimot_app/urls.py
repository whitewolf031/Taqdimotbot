from django.urls import path
from taqdimot_app.api.views import generate_work

urlpatterns = [
    path("generate-work/", generate_work, name="generate-work"),
]
