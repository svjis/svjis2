from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def main_view(request):
    # write your view processing logics here
    return render(request, "main.html", {})