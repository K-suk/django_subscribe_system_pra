from django.contrib.auth import get_user_model
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer

User = get_user_model()

class RegisterView(APIView):
    permission_classes = (permissions.AllowAny,)
    def post(self, request):
        try:
            data = request.data
            name = data['name']
            email = data['email'].lower()
            password = data['password']
            if not User.objects.filter(email=email).exists():
                User.objects.create_user(
                    name=name, email=email, password=password
                )
                return Response(
                    {'success': 'User is successfully created'},
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {'success': 'User is already registered'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        except:
            return Response(
                {'error': 'Problem happend during registering an account'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class UserView(APIView):
    def get(self, request):
        try:
            user = request.user
            user = UserSerializer(user)
            return Response(
                {'user': user.data},
                status=status.HTTP_200_OK
            )
        except:
            return Response(
                {'error': 'Problem happend during getting user info'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )