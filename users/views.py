from rest_framework.exceptions import NotFound
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
)
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from users.models import CustomUser
from users.serializers import CustomUserSerializer


class CustomUserView(APIView):
    def get_user(self, pk):
        user = CustomUser.objects.filter(id=pk).first()
        if not user:
            raise NotFound("El usuario no existe")
        return user

    def post(self, request):
        """Crear nuevo usuario
        ruta: /api/v1/users/
        metodo: post
        """
        data = request.data
        data["password"] = make_password(request.data["password"])
        serializer = CustomUserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Actualizar usuario con id = pk
        ruta: /api/v1/users/{pk}
        metodo: put
        """
        user = self.get_user(pk)
        data = request.data
        serializer = CustomUserSerializer(user, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_200_OK)
        return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Actualizar usuario con id = pk
        ruta: /api/v1/users/{pk}
        metodo: delete
        """
        user = self.get_user(pk)
        user.delete()
        user.save()
        return Response(status=HTTP_204_NO_CONTENT)
