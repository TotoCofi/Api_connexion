from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializer import UtilisateursSerializer  
from django.contrib.auth import authenticate

@api_view(['POST'])
def inscription(request):
    if request.method == 'POST':
        users_serializer = UtilisateursSerializer(data=request.data)  # Serializer les données
        if users_serializer.is_valid():
            user = users_serializer.save()

            # Générer un token d'accès et l'associer à l'utilisateur
            token, created = Token.objects.get_or_create(user=user)

            response_data = {
                'message': "l'utilisateur est enregistre avec succès",
                'user': users_serializer.data,
                'access_token': token.key,  # Renvoyer la clé du token d'accès
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        return Response({'users_errors': users_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def connexion(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'User logged in successfully', 'access_token': token.key})
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
