from django.urls import path
from main.views import create_project, show_awards

from main.views import show_main, show_experience

app_name = "main"

urlpatterns = [
    path("", show_main, name="show_main"),
    path("experience/", show_experience, name="show_experience"),
    path('awards/', show_awards, name='show_awards'),
    path("projects/add/", create_project, name="create_project"),
]