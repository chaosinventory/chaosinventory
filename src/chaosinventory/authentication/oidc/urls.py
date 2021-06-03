from django.urls import path

from .views.authorize import OIDCAuthorizeView
from .views.token import OIDCTokenView
from .views.userinfo import OIDCUserInfoView

urlpatterns = [
    path('authorize', OIDCAuthorizeView.as_view(), name="oidc_authorize"),
    path('token', OIDCTokenView.as_view(), name="oidc_token"),
    path('userinfo', OIDCUserInfoView.as_view(), name="oidc_token"),
]
