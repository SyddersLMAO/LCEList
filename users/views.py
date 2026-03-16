from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Sum
from django.core.exceptions import ValidationError
from .forms import StyledRegisterForm
from .models import User
from content.models import Content
from content.validators import validate_image_type


def register(request):
    if request.user.is_authenticated:
        return redirect('content:index')
    if request.method == 'POST':
        form = StyledRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('content:index')
    else:
        form = StyledRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    uploads = Content.objects.filter(author=profile_user, is_approved=True)
    total_downloads = uploads.aggregate(Sum('downloads'))['downloads__sum'] or 0
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'uploads': uploads,
        'total_downloads': total_downloads,
    })

@login_required
def edit_profile(request):
    if request.method == 'POST':
        user = request.user
        user.username = request.POST.get('username', '')
        user.bio = request.POST.get('bio', '')
        if 'avatar' in request.FILES:
            avatar = request.FILES['avatar']
            try:
                validate_image_type(avatar)
            except ValidationError as e:
                messages.error(request, e.message)
                return render(request, 'users/edit_profile.html', {'profile_user': user})
            user.avatar = avatar
        user.save()
        messages.success(request, 'Profile updated.')
        return redirect('users:profile', username=user.username)
    return render(request, 'users/edit_profile.html', {'profile_user': request.user})

@login_required
def delete_profile(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        return redirect('content:index')
    return redirect('users:edit_profile')