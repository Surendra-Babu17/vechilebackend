# users_app/views.py  (clean, Render/Postman friendly)
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from users_app.models import userReg
from users_app.serializers import UserRegSerializer

# ------------------------------
# Home (health check)
# ------------------------------
@csrf_exempt
@api_view(['GET'])
def home(request):
    return Response({"message": "Backend is live!"}, status=status.HTTP_200_OK)


# ------------------------------
# Register (returns 200 on success as you asked)
# ------------------------------
@csrf_exempt
@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def register(request):
    """
    Safe register:
    - uses serializer validation
    - catches IntegrityError (unique constraints)
    - returns 200 on success (per your request)
    """
    serializer = UserRegSerializer(data=request.data)
    if not serializer.is_valid():
        return Response({"success": False, "error": "validation_failed", "details": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)
    try:
        user = serializer.save()
    except IntegrityError as e:
        # Unique field violation (username/email) or DB-level constraint
        return Response({"success": False, "error": "integrity_error", "detail": str(e)},
                        status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        # Unexpected server-side error -> log and return safe message
        # (Render logs will contain traceback if you print it on server)
        return Response({"success": False, "error": "internal_server_error", "detail": str(e)},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # remove password from response if serializer included it
    data = UserRegSerializer(user).data
    data.pop('password', None)

    # Return 200 as you requested (successful registration)
    return Response({"success": True, "message": "User registered successfully", "data": data},
                    status=status.HTTP_200_OK)


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
        return Response({"success": False, "error": "email_and_password_required"},
                        status=status.HTTP_400_BAD_REQUEST)

    try:
        user = userReg.objects.get(email__iexact=email)
    except userReg.DoesNotExist:
        return Response({"success": False, "error": "invalid_credentials"},
                        status=status.HTTP_401_UNAUTHORIZED)

    if not user.check_password(password):
        return Response({"success": False, "error": "invalid_credentials"},
                        status=status.HTTP_401_UNAUTHORIZED)

    refresh = RefreshToken.for_user(user)
    access_token = str(refresh.access_token)

    user_data = UserRegSerializer(user).data
    user_data.pop('password', None)

    resp = Response({
        "success": True,
        "message": "Login successful",
        "access": access_token,
        "user": user_data
    }, status=status.HTTP_200_OK)

    resp.set_cookie(
        key='refresh_token',
        value=str(refresh),
        httponly=True,
        secure=False,   # set True on HTTPS in prod
        samesite='Lax',
        max_age=7*24*60*60
    )
    return resp


# ------------------------------
# Refresh access token
# ------------------------------
@csrf_exempt
@api_view(['POST'])
def refresh_access_token(request):
    refresh_token = request.COOKIES.get('refresh_token')
    if not refresh_token:
        return Response({"success": False, "error": "no_refresh_token"},
                        status=status.HTTP_401_UNAUTHORIZED)
    try:
        refresh = RefreshToken(refresh_token)
        new_access = str(refresh.access_token)
        return Response({"success": True, "access": new_access}, status=status.HTTP_200_OK)
    except TokenError:
        return Response({"success": False, "error": "invalid_refresh_token"},
                        status=status.HTTP_401_UNAUTHORIZED)


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
            # ignore blacklist errors, still delete cookie
            pass
    resp = Response({"success": True, "message": "Logged out"}, status=status.HTTP_200_OK)
    resp.delete_cookie('refresh_token')
    return resp


# ------------------------------
# Users CRUD (optional single endpoint)
# ------------------------------
@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def userDetails(request, id=None):
    # GET -> list or single
    if request.method == 'GET':
        if id:
            obj = userReg.objects.filter(pk=id).first()
            if not obj:
                return Response({"success": False, "error": "not_found"}, status=status.HTTP_404_NOT_FOUND)
            serializer = UserRegSerializer(obj)
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        qs = userReg.objects.all()
        serializer = UserRegSerializer(qs, many=True)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)

    # POST -> create (uses register in many apps)
    if request.method == 'POST':
        serializer = UserRegSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = serializer.save()
            except IntegrityError as e:
                return Response({"success": False, "error": "integrity_error", "detail": str(e)},
                                status=status.HTTP_400_BAD_REQUEST)
            data = UserRegSerializer(user).data
            data.pop('password', None)
            return Response({"success": True, "data": data}, status=status.HTTP_200_OK)
        return Response({"success": False, "error": "validation_failed", "details": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # PUT -> update
    if request.method == 'PUT':
        if not id:
            return Response({"success": False, "error": "id_required"}, status=status.HTTP_400_BAD_REQUEST)
        instance = userReg.objects.filter(pk=id).first()
        if not instance:
            return Response({"success": False, "error": "not_found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserRegSerializer(instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"success": True, "data": serializer.data}, status=status.HTTP_200_OK)
        return Response({"success": False, "error": "validation_failed", "details": serializer.errors},
                        status=status.HTTP_400_BAD_REQUEST)

    # DELETE -> delete
    if request.method == 'DELETE':
        if not id:
            return Response({"success": False, "error": "id_required"}, status=status.HTTP_400_BAD_REQUEST)
        instance = userReg.objects.filter(pk=id).first()
        if not instance:
            return Response({"success": False, "error": "not_found"}, status=status.HTTP_404_NOT_FOUND)
        instance.delete()
        return Response({"success": True, "message": "deleted"}, status=status.HTTP_200_OK)

    return Response({"success": False, "error": "method_not_allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
