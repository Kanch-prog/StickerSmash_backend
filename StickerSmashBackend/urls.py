from django.urls import path, include  
from django.contrib import admin
from django.contrib.auth import views as auth_views
from rest_framework.routers import DefaultRouter
from sticker_app.views import (
    StickerUploadView, StickerViewSet, admin_dashboard,
    stickers_view, duplicates_view, users_view, delete_user,assign_ward_to_admin,
    update_status, create_sticker, delete_sticker, custom_logout
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

# DRF Router for StickerViewSet
router = DefaultRouter()
router.register('api/stickers', StickerViewSet, basename='sticker')

urlpatterns = [
    # Admin and dashboard-related views
    path('admin/', admin.site.urls),  # Admin login page
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', custom_logout, name='custom_logout'),
    path('my-admin/', admin_dashboard, name='admin_dashboard'),
    path('stickers/', stickers_view, name='stickers_view'),
    path('duplicates/', duplicates_view, name='duplicates_view'),
    path('users/', users_view, name='users_view'),

    # Sticker-related actions
    path('create_sticker/', create_sticker, name='create_sticker'),
    path('update_status/<int:sticker_id>/', update_status, name='update_status'),
    path('delete_sticker/<int:id>/', delete_sticker, name='delete_sticker'),

    # User-related actions
    path('delete_user/<int:id>/', delete_user, name='delete_user'),
    path('assign_ward/<int:admin_id>/', assign_ward_to_admin, name='assign_ward_to_admin'),


    # JWT Token Endpoints
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('djoser.urls')),

    # Sticker upload
    path('api/upload/', StickerUploadView.as_view(), name='sticker-upload'),
]

# Include DRF router URLs
urlpatterns += router.urls

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
