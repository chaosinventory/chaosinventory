from django.urls import path

from .views import (
    AuthTokenDetailView, AuthTokenView, ObtainAuthTokenWithCredentialsView,
    RenewAuthTokenView,
)

urlpatterns = [
    path('token/', AuthTokenView.as_view()),
    path('token/credentials', ObtainAuthTokenWithCredentialsView.as_view()),
    path('token/renew', RenewAuthTokenView.as_view()),
    path('token/<str:id>', AuthTokenDetailView.as_view()),
]
