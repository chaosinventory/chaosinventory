from django.urls import include, path

urlpatterns = [
    path('token/', include('chaosinventory.authentication.token.urls')),
    path('oidc/', include('chaosinventory.authentication.oidc.urls'))
]
