from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import status
from .serializers import *
from .models import User, Organisation
import jwt,datetime
from .permissions import IsAdmin, IsOwner
#check if i have to send otp for verification
class UserRegisterView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer=UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    def get(self,request):
        serializer = UserSerializer(User.objects.all(), many=True)
        return Response(serializer.data)

class LoginView(APIView):
    permission_classes = []
    authentication_classes = []

    @staticmethod
    def post(request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response(
                {"detail": "Email and password are required."},
                status=HTTPStatus.BAD_REQUEST,
            )

        user = get_object_or_404(User, email=email)

        if not user.check_password(password):
            return Response(
                {"detail": "Incorrect password."}, status=HTTPStatus.BAD_REQUEST
            )


        # Generate JWT refresh token for the user
        refresh_token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)
        serializer.access_token = refresh_token.access_token
        serializer.refresh_token = str(refresh_token)

        return Response(
            {
                "data": serializer.data,
                "access_token": str(refresh_token.access_token),
                "refresh_token": str(refresh_token),
            },
            status=HTTPStatus.OK,
        )


class UserView(APIView):

    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')

        try:
            payload = jwt.decode(token, 'secret', algorithm=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

#im returning the invite code, should i make organisation name unique?
#have to make sure invite code is unique?
class CreateOrganisationView(APIView):    
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def post(self,request):
        token = request.auth
        if not token:
            return Response({'message': 'Authentication credentials not provided'}, status=401)
        print(f"Token: {token}")
        serializer=OrganisationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        organisation= serializer.save()        
        user=request.user
        user.organisation_id=organisation.id
        user.role='owner'
        user.save()       
        return Response(serializer.data['invite_code'])

class JoinOrganisationView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request):
        serializer = JoinOrganisationSerializer(data=request.data)

        if serializer.is_valid():
            invite_code = serializer.validated_data.get('invite_code')
            organisation = get_object_or_404(Organisation,invite_code=invite_code)

            user = request.user
            user.organisation_id = organisation.id
            user.role='user'
            user.save()

            return Response({'message': 'User joined the organisation successfully.'}, status=status.HTTP_200_OK)

        return Response({'message': 'Validation error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

#allowing only owner to assign admins
class ChangeRoleView(APIView):
    permission_classes = [IsAuthenticated, IsOwner]
    authentication_classes=[JWTAuthentication]

    def post(self, request):
        serializer = ChangeRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serialized_data=serializer.data
        print(serialized_data)
        user_to_change = get_object_or_404(User,email=serialized_data['email'])

        # Change the role
        user_to_change.role = serializer.data['role'].lower()
        user_to_change.save()

        return Response({'message': 'Role changed successfully'}, status=status.HTTP_200_OK)

#im allowing all admins and owners to delete users
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]
    authentication_classes=[JWTAuthentication]

    def post(self, request):
        serializer = DeleteUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # Check if the user to delete exists
        user_to_delete = get_object_or_404(User,email=serializer.data['email'])

        # Check if the user to delete has a 'user' role or lower (prevent deleting higher roles)
        #if user_to_delete.role in ['owner'] and role!= 'owner':
            #return Response({'message': 'Cannot delete higher roles'}, status=status.HTTP_403_FORBIDDEN)

        user_to_delete.delete()

        return Response({'message': 'User deleted successfully'}, status=status.HTTP_200_OK)
    
