from http import HTTPStatus
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from .serializers import UserSerializer,JoinOrganisationSerializer,OrganisationSerializer,ChangeRoleSerializer
from .models import User, Organisation
from .permissions import IsAdmin, IsOwner, IsApproved

class CheckView(APIView):
    permission_classes=[AllowAny]
    def get(self,request):
        return Response ({"message":"hi we're online"})
#---------------AUTH VIEWS---------------------

class RegisterView(APIView):
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
        username= request.data.get("username")
        
        if not username:
            if not email or not password:
                return Response(
                    {"detail": "Email and password are required."},
                    status=HTTPStatus.BAD_REQUEST,
                )

            user = get_object_or_404(User, email=email)
        elif not email:
            if not username or not password:
                return Response(
                    {"detail": "Username and password are required."},
                    status=HTTPStatus.BAD_REQUEST,
                )

            user = get_object_or_404(User, username=username)
        else:
            user=get_object_or_404(User,email=email)

        if not user.check_password(password):
            return Response(
                {"detail": "Incorrect password."}, status=HTTPStatus.BAD_REQUEST
            )


        # Generate JWT refresh token for the user
        refresh_token = RefreshToken.for_user(user)

        serializer = UserSerializer(user)
        print("Serializer Data:", serializer.data)
        serializer.access_token = refresh_token.access_token
        serializer.refresh_token = str(refresh_token)
        
        response={}
        for key in serializer.data:
            response[key]=serializer.data[key]
        response["access_token"]=str(refresh_token.access_token)
        response["refresh_token"]=str(refresh_token)
        return Response(
            {
                "data":response
                
            },
            status=HTTPStatus.OK,
        )

class LogoutView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response

#---------------USER VIEWS---------------

class UpdateDisplayUserView(APIView):
    permission_classes=[IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    
    @staticmethod
    def patch(request):
        user=get_object_or_404(User,id=request.user.id)
        serializer= UserSerializer(user,data=request.data,partial=True)
        if serializer.is_valid():
            if 'role' in serializer.validated_data:
                return Response({'detail':'You cannot change role'}, status=status.HTTP_403_FORBIDDEN)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    @staticmethod
    def get(request):
        organisation_id = request.query_params.get('org')
        if organisation_id is None:
            return Response({'detail': 'Organisation ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        users=User.objects.filter(organisation=organisation_id)
        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data, status=status.HTTP_200_OK)
    
class DeleteUserView(APIView):
    permission_classes = [IsAuthenticated,IsApproved]
    authentication_classes=[JWTAuthentication]
    def delete(self, request,user_id):
        user_to_delete=get_object_or_404(User,id=user_id)
        if user_to_delete != request.user.id or request.user.role not in ['admin','owner']:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        user_to_delete.delete()
        return Response({'message': 'POC deleted successfully'}, status=status.HTTP_200_OK)

#--------------ADMIN VIEWS--------------------

#allowing only owner to assign admins
class ChangeRoleView(APIView):
    permission_classes = [IsAuthenticated, IsOwner,IsApproved]
    authentication_classes=[JWTAuthentication]

    def post(self, request):
        serializer = ChangeRoleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_to_change = get_object_or_404(User,id=serializer.validated_data['id'])
        user_to_change.role = serializer.data['role'].lower()
        user_to_change.save()          

        return Response({'message': 'Role changed successfully'}, status=status.HTTP_200_OK)

class ApproveView(APIView):
    permission_classes = [IsAuthenticated,IsAdmin]
    authentication_classes=[JWTAuthentication]
    def post(self,request):
        user_id = request.query_params.get('user')
        if user_id is None:
            return Response({'detail': 'User ID is required'}, status=status.HTTP_400_BAD_REQUEST)
        user=get_object_or_404(User,id=user_id)
        user.is_approved=True
        user.organisation_id=request.user.organisation.id
        user.save()
        return Response({'detail':'User approved'},status=status.HTTP_200_OK)
        
#-----------ORGANISATIONS VIEWS---------------

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
        user.role='owner'
        user.is_approved=True
        user.save()       
        return Response(serializer.data)

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

            return Response({'message': 'Waiting for approval'}, status=status.HTTP_200_OK)

        return Response({'message': 'Validation error', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)




    
