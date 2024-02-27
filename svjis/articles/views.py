from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse


def main_view(request):
    return render(request, "main.html", {
        'tray_menu_items': [
            {'description': 'Články', 'link': reverse(main_view), 'active': True},
            {'description': 'Redakce', 'link': reverse(redaction_view), 'active': False},
        ],
        'aside_menu_name': 'Články',
        'aside_menu_items': [
            {'description': 'Všechny články', 'link': '/', 'active': True},
            {'description': 'Dokumenty', 'link': '/', 'active': False},
            {'description': 'Smlouvy', 'link': '/', 'active': False},
        ],
    })


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


def redaction_view(request):
    return render(request, "redaction.html", {
        'tray_menu_items': [
            {'description': 'Články', 'link': reverse(main_view), 'active': False},
            {'description': 'Redakce', 'link': reverse(redaction_view), 'active': True},
        ],
        'aside_menu_name': 'Redakce',
        'aside_menu_items': [
            {'description': 'Články', 'link': '/', 'active': True},
        ],
    })
