from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users_app.models import userReg
from users_app.serializers import UserRegSerializer

# ------------------------------
# Home / Health check
# ------------------------------
@csrf_exempt
@api_view(['GET'])
def home(request):
    return Response({"message": "Backend is live!"}, status=status.HTTP_200_OK)


# ------------------------------
# Users CRUD
# ------------------------------
@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def userDetails(request, id=None):
    # ------------------ GET ------------------
    if request.method == 'GET':
        if id:
            obj = get_object_or_404(userReg, pk=id)
            serializer = UserRegSerializer(obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
        qs = userReg.objects.all()
        serializer = UserRegSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # ------------------ POST ------------------
    if request.method == 'POST':
        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "User registered successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"error": "Register failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------ PUT ------------------
    if request.method == 'PUT':
        if not id:
            return Response({"error": "ID is required for update"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(userReg, pk=id)
        serializer = UserRegSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "User details updated", "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Update failed", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    # ------------------ DELETE ------------------
    if request.method == 'DELETE':
        if not id:
            return Response({"error": "ID is required for delete"}, status=status.HTTP_400_BAD_REQUEST)
        instance = get_object_or_404(userReg, pk=id)
        instance.delete()
        return Response({"success": "User deleted"}, status=status.HTTP_204_NO_CONTENT)

    return Response({"error": "Method not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


# ------------------------------
# Login
# ------------------------------
@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser])
def loginUser(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response({"error": "Email and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = userReg.objects.get(email__iexact=email)
    except userReg.DoesNotExist:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    serializer = UserRegSerializer(user)
    user_data = serializer.data
    user_data.pop('password', None)  # remove password from response

    resp = Response({
        "message": "Login successful",
        "access": access_token,
        "user": user_data
    }, status=status.HTTP_200_OK)

    resp.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,  # set True in production HTTPS
        samesite='Lax',
        max_age=7*24*60*60
    )
    return resp


# ------------------------------
# Refresh JWT token
# ------------------------------
@csrf_exempt
@api_view(['POST'])
def refresh_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({"error": "No refresh token found"}, status=status.HTTP_401_UNAUTHORIZED)
    try:
        refresh = RefreshToken(refresh_token)
        new_access = str(refresh.access_token)
        return Response({"access": new_access}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({"error": "Invalid refresh token"}, status=status.HTTP_401_UNAUTHORIZED)


# ------------------------------
# Logout
# ------------------------------
@csrf_exempt
@api_view(['POST'])
def logout_view(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if refresh_token:
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            pass

    resp = Response({"message": "Logged out"}, status=status.HTTP_200_OK)
    resp.delete_cookie('refresh_token')
    return resp
