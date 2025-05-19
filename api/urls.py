from django.urls import path
from users.views import LoginView


app_name = "api"
urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
]