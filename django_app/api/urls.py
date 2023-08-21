from django.urls import path

from api.users.views import UserCreateView, UserViewSet
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView


urlpatterns = [
    path('openapi/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(url_name='schema')),
    path('user/', UserCreateView.as_view()),
    path('user/<str:uuid>', UserViewSet.as_view())
]
