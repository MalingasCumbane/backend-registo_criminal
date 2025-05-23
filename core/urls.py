from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'cidadaos', views.CidadaoViewSet)
router.register(r'registros', views.RegistroCriminalViewSet)

urlpatterns = [
    path('user/me/', views.UserMeView.as_view()),
    path('dashboard/', views.DashboardView.as_view()),
    path('atividade-recente/', views.AtividadeRecenteView.as_view()),
    path('info/', views.InfoView.as_view()),
    path('', include(router.urls)),
] 