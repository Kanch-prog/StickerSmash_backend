from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView 
from django.utils.timezone import now
from django.contrib.auth.models import User
from sticker_app.models import AdminProfile 
from django.contrib import messages
from .serializers import StickerSerializer
from .models import Sticker, WARD_CHOICES  
import re
from geopy.distance import geodesic
from django.urls import reverse
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

# View for uploading a new sticker. This view saves the sticker and associates it with the logged-in user.
class StickerUploadView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = StickerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)  # Associate the sticker with the logged-in user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ViewSet for CRUD operations on stickers. It requires authentication.
class StickerViewSet(viewsets.ModelViewSet):
    queryset = Sticker.objects.all()
    serializer_class = StickerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.groups.filter(name="Super_Admin").exists():
            return Sticker.objects.all()  # Super_Admin sees all stickers
        elif user.groups.filter(name="Ward_Admin").exists():
            # If user is a ward_admin, filter by assigned ward (use AdminProfile if created)
            admin_profile = user.adminprofile  # Assuming AdminProfile model
            return Sticker.objects.filter(ward=admin_profile.ward)
        return Sticker.objects.none()


# Admin dashboard view with stickers and users. Only staff can access this page.
@staff_member_required
def admin_dashboard(request):
    user = request.user

    if user.groups.filter(name="Super_Admin").exists():
        stickers = Sticker.objects.all()  # Super_Admin sees all stickers
        admins = User.objects.filter(groups__name="Ward_Admin")  # Show all Ward_Admin users
    elif user.groups.filter(name="Ward_Admin").exists():
        stickers = Sticker.objects.filter(ward=user.adminprofile.ward)  # Ward_Admin sees only their ward
        admins = None  # They don't manage other admins
    else:
        stickers = Sticker.objects.none()
        admins = None

    return render(request, 'base.html', {'stickers': stickers, 'admins': admins})

# View for displaying all stickers in a table. 
@staff_member_required
def stickers_view(request):
    user = request.user

    if user.groups.filter(name="Super_Admin").exists():
        stickers = Sticker.objects.all()
    elif user.groups.filter(name="Ward_Admin").exists():
        stickers = Sticker.objects.filter(ward=user.adminprofile.ward)  # Filter by assigned ward
    else:
        stickers = Sticker.objects.none()  # No access

    return render(request, 'sticker_table.html', {'stickers': stickers})


# View to display duplicate stickers found based on proximity and description matching.
@staff_member_required
def duplicates_view(request):
    stickers = Sticker.objects.all()  # Fetch all stickers
    duplicates = find_duplicates(stickers)  # Find duplicate stickers
    return render(request, 'duplicates_table.html', {'duplicates': duplicates})

# View to display all users. Admins can see this data.
@staff_member_required
def users_view(request):  
    user = request.user
    
    if not user.groups.filter(name="Super_Admin").exists():
        messages.error(request, "You are not authorized to assign wards.")
        return redirect('admin_dashboard')

    users = User.objects.all()
    return render(request, 'user_table.html', {'users': users, 'wards': WARD_CHOICES})


# Common keywords used to identify potential duplicates (e.g., "leak", "flood", etc.)
COMMON_KEYWORDS = {"pipe", "garbage", "leak", "traffic", "pot holes", "water", "damage", "flood", "drain", "waste"}

# Checks if a description contains any of the common keywords.
def contains_common_keywords(description):
    description = description.lower()
    return any(keyword in description for keyword in COMMON_KEYWORDS)

# Function to find duplicate stickers based on description and proximity
def find_duplicates(stickers):
    duplicates = []
    checked_pairs = set()  # To store already compared pairs
    
    for i, sticker in enumerate(stickers):
        for j, other_sticker in enumerate(stickers):
            if i >= j:  # Avoid comparing the same pair twice
                continue

            if contains_common_keywords(sticker.description) and contains_common_keywords(other_sticker.description):
                if sticker.category == other_sticker.category:
                    if sticker.latitude and other_sticker.latitude and sticker.longitude and other_sticker.longitude:
                        # Calculate distance between two stickers
                        distance = geodesic((sticker.latitude, sticker.longitude), (other_sticker.latitude, other_sticker.longitude)).km
                        if distance < 1:  # Consider issues within 1 km as potential duplicates
                            # Add to duplicates if not already added
                            if (sticker.id, other_sticker.id) not in checked_pairs and (other_sticker.id, sticker.id) not in checked_pairs:
                                duplicates.append((sticker, other_sticker))
                                checked_pairs.add((sticker.id, other_sticker.id))  # Mark this pair as checked
    return duplicates

# Function to delete a sticker by its ID (admin only).
def delete_sticker(request, id):
    if request.method == 'POST':
        sticker = get_object_or_404(Sticker, id=id)
        sticker.delete()
        messages.success(request, 'Sticker deleted successfully.')  # Optionally, add a success message
    return redirect('admin_dashboard')


# Function to delete a user by their ID (admin only).
def delete_user(request, id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=id)
        user.delete()
    return redirect('admin_dashboard')


# Admin view to update the status of a sticker
def update_status(request, sticker_id):
    if request.method == 'POST':
        sticker = get_object_or_404(Sticker, id=sticker_id)
        new_status = request.POST.get('status')
        if new_status in dict(Sticker.STATUS_CHOICES).keys():
            sticker.status = new_status
            sticker.save()
            messages.success(request, 'Status updated successfully.')
        else:
            messages.error(request, 'Invalid status value.')
    return redirect('admin_dashboard')

def custom_logout(request):
    # Logs the user out of both the app and the Django admin
    logout(request)
    return redirect('/admin/login/')  # Redirect to the login page after logout


# Function to create a new sticker. Authenticated users can report stickers.
def create_sticker(request):
    if request.method == 'POST':
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        description = request.POST.get('description')

        # Save the sticker
        sticker = Sticker(
            user=request.user,
            latitude=latitude,
            longitude=longitude,
            description=description,
            category=request.POST.get('category'),
            priority=request.POST.get('priority'),
        )
        sticker.save()
        return redirect('dashboard')

    return render(request, 'create_sticker.html')

@login_required
@staff_member_required
def assign_ward_to_admin(request, admin_id):
    admin_user = get_object_or_404(User, id=admin_id)

    if not request.user.groups.filter(name="Super_Admin").exists():
        messages.error(request, "You are not authorized to assign wards.")
        return redirect('admin_dashboard')

    if not admin_user.groups.filter(name="Ward_Admin").exists():
        messages.error(request, "Only Ward_Admins can be assigned wards.")
        return redirect('users_view')

    if request.method == 'POST':
        ward = request.POST.get('ward')
        if ward in dict(WARD_CHOICES).keys():
            admin_profile, created = AdminProfile.objects.get_or_create(user=admin_user)
            admin_profile.ward = ward
            admin_profile.save()
            messages.success(request, f'Ward "{ward}" assigned to {admin_user.username} successfully!')
        else:
            messages.error(request, 'Invalid ward selected.')

    return redirect('users_view')
