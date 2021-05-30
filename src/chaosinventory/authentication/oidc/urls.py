from django.urls import path

from .views.authorize import OIDCAuthorizeView
from .views.token import OIDCTokenView

urlpatterns = [
    path('authorize', OIDCAuthorizeView.as_view(), name="oidc_authorize"),
    path('token', OIDCTokenView.as_view(), name="oidc_token"),
]
