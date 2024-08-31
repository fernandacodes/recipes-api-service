from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from rowcipes_registry.views.auth_view import (
    register_user, get_user,
)
from rowcipes_registry.views.receita_view import *
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token

urlpatterns = [
    path('api/register/', register_user),
    path('api/token/', obtain_jwt_token),
    path('api/user/', get_user),
    path('api/token/refresh/', refresh_jwt_token),
    path('api/token/verify/', verify_jwt_token),
    path('receitas/', create_receita, name='create_receita'),
    path('receitas/all/', get_all_receitas, name='get_all_receitas'),
    path('receitas/<int:receita_id>/', get_receita_by_id, name='get_receita_by_id'),
    path('receitas/update/<int:receita_id>/', update_receita, name='update_receita'),
    path('receitas/search/', search_receitas_by_name, name='search_receitas_by_name'),
    path('receitas/user/<int:user_id>/', get_receitas_by_user, name='get_receitas_by_user'),

]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
