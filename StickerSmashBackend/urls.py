from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from sticker_app.views import StickerUploadView, StickerViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'stickers', StickerViewSet)  # Register the viewset

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('sticker_app.urls')), 
    path('api/upload/', StickerUploadView.as_view(), name='sticker-upload'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.jwt')),  # JWT auth URLs
    path('api/', include(router.urls)),  # Include router URLs
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
