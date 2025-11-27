from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users_app.models import userReg, clientReg
from users_app.serializers import UserRegSerializer, ClientRegSerializer


# ---------- Home route ----------
@csrf_exempt
@api_view(['GET'])
def home(request):
    """
    Simple health check or home endpoint
    """
    return Response({"message": "Backend is live!"}, status=status.HTTP_200_OK)


# ---------- Users CRUD (list/create/update/delete) ----------
@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def userDetails(request, id=None):
    # GET -> list all or single
    if request.method == 'GET':
        if id:
            obj = get_object_or_404(userReg, pk=id)
            serializer = UserRegSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        qs = userReg.objects.all()
        serializer = UserRegSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # POST -> create new user
    if request.method == 'POST':
        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "register failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # PUT -> update user
    if request.method == 'PUT':
        if not id:
            return Response({"error": "id is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(userReg, pk=id)
        serializer = UserRegSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "user details updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "user details not updated", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # DELETE -> delete user
    if request.method == 'DELETE':
        if not id:
            return Response({"error": "id is required for delete"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(userReg, pk=id)
        instance.delete()
        return Response({"success": "user deleted"}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error": "method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ---------- Login view ----------
@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def loginUser(request):
    data = request.data
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return Response({"success": "Email and password are required"}, status=400)

    try:
        user = userReg.objects.get(email__iexact=email)
    except userReg.DoesNotExist:
        return Response({"success": "Invalid credentials"}, status=401)

    if not user.check_password(password):
        return Response({"success": "Invalid credentials"}, status=401)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    serializer = UserRegSerializer(user)
    user_data = serializer.data
    user_data.pop('password', None)

    resp = Response({
        "message": "Login successful",
        "access": access_token,
        "user": user_data
    }, status=200)

    resp.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=7*24*60*60
    )
    return resp


# ---------- Refresh access token ----------
@csrf_exempt
@api_view(['POST'])
def refresh_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({"detail": "No refresh token"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        refresh = RefreshToken(refresh_token)
        new_access = str(refresh.access_token)
        return Response({"access": new_access}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({"detail": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


# ---------- Logout view ----------
@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({"detail": "No refresh token"}, status=status.HTTP_400_BAD_REQUEST)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception:
        pass
    resp = Response({"detail": "Logged out"}, status=status.HTTP_200_OK)
    resp.delete_cookie('refresh_token')
    return resp
