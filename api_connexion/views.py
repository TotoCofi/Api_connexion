from .models import Utilisateurs
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializer import UtilisateursSerializer  
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated


@api_view(['POST'])
def inscription(request):
    if request.method == 'POST':
        users_serializer = UtilisateursSerializer(data=request.data)  # Serializer les données
        if users_serializer.is_valid():
            user = users_serializer.save()
            user.set_password(request.data['password'])
            user.is_active = True

            user.save()

            # Générer un token d'accès et l'associer à l'utilisateur
            token, created = Token.objects.get_or_create(user=user)

          
            return Response({
                'message': "l'utilisateur est enregistre avec succès",
                'user': users_serializer.data,
                'access_token': token.key, 
            }, status=status.HTTP_201_CREATED)
        else:
            print(users_serializer.errors)

        return Response({'users_errors': users_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def connexion(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')

        user = Utilisateurs.objects.get(username=username)

        if user.check_password(password):
            token, created = Token.objects.get_or_create(user=user)
            return Response({'message': 'Connexion réusir', 'access_token': token.key})
        else:
            return Response({'message': 'Les donnée ne corrrespond'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def afficher_profil(request):
    user = request.user
    user_serializer = UtilisateursSerializer(user)  # Supposant que vous avez un serializer pour le modèle Utilisateur

    response_data = {
        'message': 'Pofile de Utilisateur',
        'user_profile': user_serializer.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deconnexion(request):
    user = request.user
    try:
        token = Token.objects.get(user=user)
        token.delete()  # Supprime le token d'accès associé à l'utilisateur
        return Response({'message': 'utilisateur deconnecte'}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"message': 'utilisateur n'existe pas"}, status=status.HTTP_400_BAD_REQUEST)
