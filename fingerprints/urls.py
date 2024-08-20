from django.urls import path
from .views import MatchFingerprintView

urlpatterns = [
    path('match/', MatchFingerprintView.as_view(), name='match-fingerprint'),
]