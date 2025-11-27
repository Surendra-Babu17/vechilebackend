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
    path('', views.home, name='home'),  # <-- home route
    path('register/', views.userDetails),
    path('login/', views.loginUser),
    path('api/refresh/', views.refresh_access_token),
    path('api/logout/', views.logout_view),
]

