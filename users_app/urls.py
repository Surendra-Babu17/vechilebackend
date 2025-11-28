# from django.urls import path
# from users_app import views

# urlpatterns = [
#     path('register/', views.userDetails),
#     path('register/<int:id>/', views.userDetails),
#     path('login/',views.loginUser),
#     path('api/refresh/', views.refresh_access_token),
#     path('api/logout/', views.logout_view),

# ]

from django.urls import path
from users_app import views

urlpatterns = [
    path('', views.home, name='home'),                     # Health check
    path('register/', views.register, name='register'),    # Correct register view
    path('login/', views.loginUser, name='login'),         # Login
    path('refresh/', views.refresh_access_token, name='refresh'),  # Token refresh
    path('logout/', views.logout_view, name='logout'),     # Logout

    # CRUD
    path('users/', views.userDetails, name='users_list'),
    path('users/<int:id>/', views.userDetails, name='user_detail'),
]
