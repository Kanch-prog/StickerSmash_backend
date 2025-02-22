# sticker_app/urls.py
from django.urls import path
from .views import (
    StickerUploadView, TokenObtainPairView, TokenRefreshView, admin_dashboard, 
    delete_sticker, delete_user, update_status
)

urlpatterns = [
    path('upload/', StickerUploadView.as_view(), name='sticker-upload'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView, name='token_refresh'),
    path('delete-sticker/<int:id>/', delete_sticker, name='delete_sticker'),
    path('delete-user/<int:id>/', delete_user, name='delete_user'),
    path('update-status/<int:sticker_id>/', update_status, name='update_status'),
]