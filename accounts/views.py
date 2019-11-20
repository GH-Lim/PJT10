from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .forms import CustomUserCreationForm


def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:userlist')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('accounts:userlist')
    else: # == 'GET'
        form = CustomUserCreationForm()
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:userlist')
    
    form = AuthenticationForm(request, request.POST or None)
    if form.is_valid():
        auth_login(request, form.get_user())
        next_page = request.GET.get('next')
        return redirect(next_page or 'accounts:userlist')
    context = {'form': form}
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect('accounts:login')


def userlist(request):
    users = get_user_model().objects.all()
    context = {
        'users': users,
    }
    return render(request, 'accounts/userlist.html', context)


def userdetail(request, user_pk):
    user = get_object_or_404(get_user_model(), pk=user_pk)
    # movies = user.liked_movies.all()
    # reviews = user.reviews.all()
    context = {
        'user': user,
        # 'movies': movies,

    }
    return render(request, 'accounts/userdetail.html', context)
