from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout


def main_view(request):
    # write your view processing logics here
    return render(request, "main.html", {})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
    return redirect(main_view)


def user_logout(request):
    logout(request)
    return redirect(main_view)