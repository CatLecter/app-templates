from rest_framework.generics import RetrieveUpdateDestroyAPIView, CreateAPIView

from api.users.serializers import UserSerializer
from users.models import User


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
