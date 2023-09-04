from api.users.serializers import UserSerializer
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from users.models import User


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'uuid'
