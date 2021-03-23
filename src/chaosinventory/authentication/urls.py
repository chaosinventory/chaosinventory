from django.urls import path

from .views import (
    AuthTokenView, ObtainAuthTokenWithCredentialsView, RenewAuthTokenView,
)

urlpatterns = [
    path('token', AuthTokenView.as_view()),
    path('token/credentials', ObtainAuthTokenWithCredentialsView.as_view()),
    path('token/renew', RenewAuthTokenView.as_view()),
]
