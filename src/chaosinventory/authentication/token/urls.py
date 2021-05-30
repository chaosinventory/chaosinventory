from django.urls import path

from .views import (
    AuthTokenDetailView, AuthTokenView, ObtainAuthTokenWithCredentialsView,
    RenewAuthTokenView,
)

urlpatterns = [
    path('', AuthTokenView.as_view()),
    path('credentials', ObtainAuthTokenWithCredentialsView.as_view()),
    path('renew', RenewAuthTokenView.as_view()),
    path('<str:id>', AuthTokenDetailView.as_view())
]
