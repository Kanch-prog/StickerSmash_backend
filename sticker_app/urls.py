# sticker_app/urls.py
from django.urls import path
from .views import StickerUploadView, MyTokenObtainPairView, token_refresh_view, admin_dashboard, delete_sticker, delete_user


urlpatterns = [
    path('upload/', StickerUploadView.as_view(), name='sticker-upload'),
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', token_refresh_view, name='token_refresh'),    
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
    path('delete-sticker/<int:id>/', delete_sticker, name='delete_sticker'),
    path('delete-user/<int:id>/', delete_user, name='delete_user'),
]
