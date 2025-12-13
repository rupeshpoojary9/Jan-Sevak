from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ComplaintViewSet, WardViewSet, LeaderboardViewSet
from . import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r'complaints', ComplaintViewSet)
router.register(r'wards', WardViewSet)
router.register(r'leaderboard', LeaderboardViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
    path('resolve/<int:pk>/<str:token>/', views.resolve_complaint, name='resolve_complaint'),
]