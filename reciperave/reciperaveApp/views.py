from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, redirect
from django.db import connection
from datetime import *
import datetime
from django.forms import pform
from django.models import upload
# Create your views here.

def login(request):
    return render(request, 'login.html')
    
def register(request):
    return render(request, 'register.html')
    
def feedback(request):
    return render(request, 'feedback.html')
    
def upload(request):
    return render(request, 'upload.html')

def registerForm(request):
    cursor = connection.cursor()
    fname = request.GET['fname']
    lname = request.GET['lname']
    uname = request.GET['username']
    email = request.GET['email']
    password = request.GET['password']
    sql = "INSERT INTO register(fname, lname, username, email) VALUES('%s', '%s', '%s', '%s')"%(fname, lname, username, email)
    cursor.execute(sql)
    sql2 = "SELECT MAX(uid) AS uid FROM register"
    cursor.execute(sql2)
    rs = cursor.fetchall()
    for row in rs:
        sql3 = "INSERT INTO login(uid, username, password, utype) VALUES('%s', '%s', '%s', 'user')"%(row[0], username, password)
        cursor.execute(sql3)
    msg = "<script>alert('Successfull');window.location='/upload/'</script>"
    return HttpResponse(msg)
    
def loginForm(request):
    cursor = connection.cursor()
    uname = request.GET['username']
    password = request.GET['password']
    s = "SELECT * FROM login WHERE username='%s' AND password='%s'"%(uname, password)
    cursor.execute(s)
    if (cursor.rowcount) > 0:
        rs = cursor.fetchall()
        for row in rs:
            request.session['uid'] = row[1]
            request.session['utype'] = row[4]
            if (request.session['utype'] == "admin"):
                return render(request, "adminHome.html")        
            elif request.session['utype'] == "user":
                return render(request, "userHome.html")
            else:
                h = "<script>alert('Login Failed');window.location='/login/'</script>"
                return HttpResponse(h)
        else:
            msg = "<script>alert('Login Failed');window.location='/login/'</script>"
            return HttpResponse(msg)
            
def feedback(request):
    cursor = connection.cursor()
    uid = request.session['uid']
    mess = request.session['message']
    sql = "INSERT INTO feedback(uid, message) VALUES('%s', '%s')"%(uid, mess)
    cursor.execute(sql)
    h = "<script>alert('Feedback Successful');window.location='/userHome/';</script>"
    return HttpResponse(h)
    
def uploadForm(request):
    if request.method == "POST":
        MyUploadForm = pform(request.POST, request.FILES)
        if MyUploadForm.is_valid():
            data = upload()
            data.recipe_name = MyUploadForm.cleaned_data["recipe_name"]
            data.total_time = request.POST["total_time"]
            data.dishType = request.POST["dishType"]
            data.description = request.POST["description"]
            data.photo_video = MyUploadForm.cleaned_data["photo_video"]
            data.instruction = request.POST["instruction"]
            data.uid = request.session["uid"]
            data.save()
            msg = "<script>alert('successfull');window.location='/index/'</script>"
            saved = True
            
    else:
        MyUploadForm = pform()
    return HttpResponse(msg)