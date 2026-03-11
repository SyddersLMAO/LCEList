from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import StyledRegisterForm
from .models import User
from content.models import Content


def register(request):
    if request.user.is_authenticated:
        return redirect('content:index')
    if request.method == 'POST':
        form = StyledRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created — you can now log in.')
            return redirect('users:login')
    else:
        form = StyledRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    uploads = Content.objects.filter(author=profile_user, is_approved=True)
    return render(request, 'users/profile.html', {
        'profile_user': profile_user,
        'uploads': uploads,
    })