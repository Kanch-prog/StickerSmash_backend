from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404, redirect
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import StickerSerializer, MyTokenObtainPairSerializer
from .models import Sticker
from rest_framework import viewsets
from django.shortcuts import render
from django.contrib.auth.models import User

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

@api_view(['POST'])
@permission_classes([AllowAny])
def token_refresh_view(request):
    return TokenRefreshView.as_view()(request)

class StickerUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StickerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StickerViewSet(viewsets.ModelViewSet):
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer

def admin_dashboard(request):
    stickers = Sticker.objects.all()
    users = User.objects.all()
    return render(request, 'admin_dashboard.html', {
        'stickers': stickers,
        'users': users
    })

def delete_sticker(request, id):
    if request.method == 'POST':
        sticker = get_object_or_404(Sticker, id=id)
        sticker.delete()
    return redirect('admin_dashboard')

def delete_user(request, id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=id)
        user.delete()
    return redirect('admin_dashboard')