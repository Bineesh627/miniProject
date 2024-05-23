from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect
from django.db import connection
from datetime import *
import datetime
# Create your views here.

def upload(request):
    return render(request, 'upload.html')
