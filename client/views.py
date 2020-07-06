from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm





def home(request):
     return render(request,'index.html')