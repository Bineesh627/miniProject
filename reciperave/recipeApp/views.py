from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect, HttpResponseRedirect
from django.db import connection
from datetime import *
import datetime
from recipeApp.models import upload1
from recipeApp.forms import pform

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def feedback(request):
    return render(request, 'feedback.html')

def userhome(request):
    cur = connection.cursor()
    
    uid = request.session['uid']
    
    # Get all users except the current user
    s = "SELECT * FROM registration WHERE uid != %s"
    cur.execute(s, [uid])
    
    list1 = []
    result = cur.fetchall()
    
    # Get a list of all users that the current user is following
    follow_query = "SELECT uid1 FROM tbl_follow WHERE uid2 = %s"
    cur.execute(follow_query, [uid])
    following = {row[0] for row in cur.fetchall()}

    for row in result:
        w = {
            'uid': row[0],
            'fname': row[1],
            'lname': row[2],
            'username': row[3],
            'is_following': row[0] in following  # Check if already following
        }
        list1.append(w)

    return render(request, 'userhome.html', {'list1': list1})

def adminhome(request):
    return render(request, 'adminhome.html')

def recipeForm(request):
    return render(request, 'viewrecipeform.html')

def userProfile(request):
    return render(request, 'userProfile.html')

def uploadn(request):
    cur = connection.cursor()
    s = "SELECT * FROM categorys"
    cur.execute(s)
    list2 = []
    result = cur.fetchall()
    for row in result:
        w = {'cid': row[0], 'dishtype': row[1]}
        list2.append(w)
    s1="select * from recipe"
    cur.execute(s1)
    list1 = []
    result = cur.fetchall()
    for row1 in result:
        q = {'rcid': row1[0], 'uid': row1[1],'recipe_name': row1[2],'total_time': row1[3],'dishtype': row1[4],'description': row1[5]}
        list1.append(q)
    return render(request, 'uploadn.html', {'list2': list2,'list1':list1})

def registerForm(request):
    # Establishing a cursor object from the database connection
    cursor = connection.cursor()
    # Retrieving form data from the request
    fname = request.GET['fname']
    lname = request.GET['lname']
    uname = request.GET['username']
    email = request.GET['email']
    password = request.GET['password']
    phone = request.GET['phone']
    # Inserting the registration details into the registration table
    sql = "INSERT INTO registration(fname, lname, username, email, phone) VALUES('%s', '%s', '%s', '%s', '%s')"%(fname, lname, uname, email, phone)
    cursor.execute(sql)
    # Retrieving the maximum user ID (uid) ro
    sql2 = "SELECT MAX(uid) AS uid FROM registration"
    cursor.execute(sql2)
    rs = cursor.fetchall()
    for row in rs:
        sql3 = "INSERT INTO login(uid, username, password, utype) VALUES('%s', '%s', '%s', 'user')"%(row[0], uname, password)
        cursor.execute(sql3)
    msg = "<script>alert('successfull');window.location='/login/'</script>"
    return HttpResponse(msg)

def userLogin(request):
    cursor = connection.cursor()
    uname = request.GET['username']
    upass = request.GET['password']
    s = "SELECT * FROM login WHERE username='%s' AND password='%s'"%(uname, upass)
    cursor.execute(s)
    if (cursor.rowcount) > 0:
        rs = cursor.fetchall()
        for row in rs:
            request.session['uid'] = row[1]
            request.session['utype'] = row[4]
        if (request.session['utype'] == "admin"):
            return render(request, 'adminhome.html')
        elif request.session['utype'] == "user":
            return render(request, 'userhome.html')
        else:
            h = "<script>alert('Login failed');window.location='/login/';</script>"
            return HttpResponse(h)
    else:
        msg = "<script>alert('Login failed');window.location='/login/';</script>"
        return HttpResponse(msg)

def feedbackForm(request):
    cursor = connection.cursor()
    uid = request.session['uid']
    mess = request.GET['message']
    sql = "INSERT INTO feedback(uid, message) VALUES('%s', '%s')"%(uid, mess)
    cursor.execute(sql)
    h = "<script>alert('Feedback Successful');window.location='/userHome/';</script>"
    return HttpResponse(h)

def uploadForm(request):
    if request.method == "POST":
        MyForm1 = pform(request.POST, request.FILES)
        if MyForm1.is_valid():
            data = upload1()
            data.recipe_name = MyForm1.cleaned_data["recipe_name"]
            data.total_time = request.POST["total_time"]
            data.dishType = request.POST["dishType"]
            data.description = request.POST["description"]
            data.photo_video = MyForm1.cleaned_data["photo_video"]
            data.instruction = request.POST["instruction"]
            data.uid=request.session['uid']
            data.save()
            
            msg = "<script>alert('successfull');window.location='/index/'</script>"
            saved = True
    else:
        MyForm1 = pform()
    return HttpResponse(msg)


def uploadnForm(request):
    cursor = connection.cursor()
    uid = request.session['uid']
    rec = request.GET['recipe_name']
    tot = request.GET['total_time']
    dis = request.GET['dishtype']
    des = request.GET['description']
    sql = "INSERT INTO recipe(uid,recipe_name,total_time,dishtype,description) VALUES('%s', '%s','%s','%s','%s')"%(uid,rec,tot,dis,des)
    cursor.execute(sql)
    h = "<script>alert('upload Successful');window.location='/uploadn/';</script>"
    return HttpResponse(h)




def viewreg(request):
    cur = connection.cursor()
    s = "SELECT * FROM registration"
    cur.execute(s)
    lists = []
    result = cur.fetchall()
    for row in result:
        w = {'uid': row[0], 'fname': row[1], 'lname': row[2], 'username': row[3], 'email': row[4], 'phone': row[5]}
        lists.append(w)
    return render(request, 'viewreg.html', {'lists': lists})

def viewfeedback(request):
    cur = connection.cursor()
    s = "SELECT * FROM feedback INNER JOIN registration ON registration.uid = feedback.uid"
    cur.execute(s)
    messages = []
    result = cur.fetchall()
    for row in result:
        w = {'fid': row[0], 'uid': row[1], 'message': row[2], 'name': row[4]}
        messages.append(w)
    return render(request, 'viewfeedback.html', {'messages': messages})

def categorys(request):
    cur = connection.cursor()
    s = "SELECT * FROM categorys"
    cur.execute(s)
    list = []
    result = cur.fetchall()
    for row in result:
        w = {'cid': row[0], 'dishtype': row[1]}
        list.append(w)
    return render(request, 'categorys.html', {'list': list})

def categoryForm(request):
    cursor = connection.cursor()
    catgys = request.GET['cat']
    sql = "INSERT INTO categorys(dishtype) VALUES('%s')"%(catgys)
    cursor.execute(sql)
    h = "<script>alert('category add Successful');window.location='/categorys/';</script>"
    return HttpResponse(h)

def viewrecipe(request):
    cursor = connection.cursor()
    s = "SELECT * FROM recp"
    cursor.execute(s)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'dishtype': row[4], 'description': row[5], 'photo_video': row[6], 'instruction': row[7]}
        list.append(w)
    return render(request, 'viewrecipe.html', {'list': list})

def deleterecipe(request):
    cursor = connection.cursor()
    id = request.GET['id']
    sql1 = "DELETE FROM recp WHERE rid='%s'"%(id)
    cursor.execute(sql1)
    msg = "<script>alert('Successfully Deleted');window.location=/viewrecipe/;</script>"
    return HttpResponse(msg)

def upload(request):
    # id = request.GET['id']
    cursor = connection.cursor()
    s = "SELECT * FROM categorys"
    cursor.execute(s)
    list1 = []
    result1 = cursor.fetchall()
    for row in result1:
        w1 = {'cid': row[0], 'dishtype': row[1]}
        list1.append(w1)
    sql1 = "SELECT * FROM recp"
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'dishtype': row[4], 'description': row[5], 'photo_video': row[6], 'instruction': row[7]}
        list.append(w)
    return render(request, 'upload.html', {'list': list, 'id': id,'list1': list1})

def updaterecipe(request):
    id = request.GET['id']
    cursor = connection.cursor()
    sql1 = "SELECT * FROM recp"
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'dishtype': row[4], 'description': row[5], 'instruction': row[7]}
        list.append(w)
    return render(request, 'updaterecipe.html', {'list': list, 'id': id})

def updateRecipeAction(request):
    cursor = connection.cursor()
    id = request.GET['id']
    rname = request.GET['recipe_name']
    ttime = request.GET['total_time']
    desc = request.GET['description']
    instr = request.GET['instruction']
    s = "UPDATE recp SET recipe_name='%s', total_time='%s', description='%s', instruction='%s' WHERE rid='%s'"%(rname, ttime, desc, instr, id)
    cursor.execute(s)
    msg = "<script>alert('Successfully Updated');window.location='/upload/';</script>"
    return HttpResponse(msg)

def updaten(request):
    id = request.GET['id']
    cursor = connection.cursor()
    sql1 = "SELECT * FROM recipe"
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rcid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'description': row[5]}
        list.append(w)
    return render(request, 'updaten.html', {'list': list, 'id': id})

def updatenAction(request):
    cursor = connection.cursor()
    id = request.GET['id']
    rname = request.GET['recipe_name']
    ttime = request.GET['total_time']
    desc = request.GET['description']
    # instr = request.GET['instruction']
    s = "UPDATE recipe SET recipe_name='%s', total_time='%s', description='%s' WHERE rcid='%s'"%(rname, ttime, desc, id)
    cursor.execute(s)
    msg = "<script>alert('Successfully Updated');window.location='/uploadn/';</script>"
    return HttpResponse(msg)

def deleten(request):
    cursor = connection.cursor()
    id = request.GET['id']
    sql1 = "DELETE FROM recipe WHERE rcid='%s'"%(id)
    cursor.execute(sql1)
    msg = "<script>alert('Successfully Deleted');window.location=/uploadn/;</script>"
    return HttpResponse(msg)

def userRecipeView(request):
    # id = request.GET['id']
    cursor = connection.cursor()
    sql1 = "SELECT * FROM recp"
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'dishtype': row[4], 'description': row[5], 'photo_video': row[6], 'instruction': row[7]}
        list.append(w)
    return render(request, 'userRecipeView.html', {'list': list})

def textrec(request):
    # id = request.GET['id']
    cursor = connection.cursor()
    sql1 = "SELECT * FROM recipe"
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rcid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'dishtype': row[4], 'description': row[5]}
        list.append(w)
    return render(request, 'textrec.html', {'list': list})

def newRecipeSearch(request):
    cursor = connection.cursor()
    pname = request.GET['pname']
    sql1 = "SELECT * FROM recp WHERE recipe_name='%s'"%(pname)
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'dishtype': row[4], 'description': row[5], 'photo_video': row[6], 'instruction': row[7]}
        list.append(w)
    return render(request, 'userRecipeView.html', {'list': list})

def TrecipeSearch(request):
    cursor = connection.cursor()
    pname = request.GET['pname']
    sql1 = "SELECT * FROM recipe WHERE recipe_name='%s'"%(pname)
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'rcid': row[0], 'uid': row[1], 'recipe_name': row[2], 'total_time': row[3], 'dishtype': row[4], 'description': row[5]}
        list.append(w)
    return render(request, 'textrec.html', {'list': list})


def profileUpdate(request):
    cursor = connection.cursor()
    uid = request.session['uid']
    sql1 = "SELECT * FROM registration WHERE uid='%s'"%(uid)
    cursor.execute(sql1)
    list = []
    result = cursor.fetchall()
    for row in result:
        w = {'uid': row[0], 'username': row[3], 'email': row[4]}
        list.append(w)
    return render(request, 'profileUpdate.html', {'list': list, 'id': id})


def profileUpdateAction(request):
    cursor = connection.cursor()
    id = request.GET['id']
    username = request.GET['username']
    email = request.GET['email']
    s = "UPDATE registration SET username='%s', email='%s' WHERE uid='%s'"%(username, email, id)
    l = "UPDATE login SET username='%s' WHERE uid='%s'"%(username, id)
    cursor.execute(s)
    cursor.execute(l)
    msg = "<script>alert('Profile Successfully Updated');window.location='/userProfile/';</script>"
    return HttpResponse(msg)

def forgetpassword(request):
    return render(request, "forgetpassword.html")

def forgetAction(request):
    cursor = connection.cursor()
    email =  request.GET['email']
    phone = request.GET['phone']
    s1 = "SELECT uid FROM registration WHERE email='%s' AND phone='%s'"%(email, phone)
    cursor.execute(s1)
    result = cursor.fetchall()
    for row in result:
        s2 = "SELECT password FROM login WHERE uid='%s'"%(row[0])
        cursor.execute(s2)
        result2 = cursor.fetchall()
    return render(request, 'forgetpassword.html', {'result2': result2})

def viewprof(request):
    cur = connection.cursor()
    s = "SELECT * FROM registration"
    cur.execute(s)
    lists = []
    result = cur.fetchall()
    for row in result:
        w = {'uid': row[0], 'fname': row[1], 'lname': row[2], 'username': row[3]}
        lists.append(w)
    return render(request, 'viewprof.html', {'lists': lists})
def followUser(request):
    cursor = connection.cursor()
    uid2 = request.session['uid']  # User ID of the current session user (follower)
    uid1 = request.GET['id']       # User ID of the user to be followed
    
    sql = "INSERT INTO tbl_follow(uid1, uid2) VALUES(%s, %s)"
    cursor.execute(sql, [uid1, uid2])

    
    
    h = "<script>alert('Follow request sent successfully');window.location='/userhome/';</script>"
    return HttpResponse(h)


def uvfollow(request):
    cur = connection.cursor()
    
    # Retrieve the user ID from the session
    uid = request.session['uid']
    
    # Get the followers of the user
    s = """
        SELECT r.uid, r.fname, r.lname, r.username 
        FROM tbl_follow f
        INNER JOIN registration r ON f.uid2 = r.uid 
        WHERE f.uid1 = %s
    """
    
    cur.execute(s, [uid])
    lists = []
    
    result = cur.fetchall()
    
    # Get a list of users that the current user is following
    follow_query = "SELECT uid1 FROM tbl_follow WHERE uid2 = %s"
    cur.execute(follow_query, [uid])
    following_back = {row[0] for row in cur.fetchall()}

    for row in result:
        w = {
            'uid': row[0],
            'fname': row[1],
            'lname': row[2],
            'username': row[3],
            'is_following_back': row[0] in following_back
        }
        lists.append(w)
    
    return render(request, 'uvfollow.html', {'lists': lists})

def followBackUser(request):
    cursor = connection.cursor()
    uid2 = request.session['uid']  # User ID of the current session user (follower)
    uid1 = request.GET['id']       # User ID of the user to be followed
    
    sql = "INSERT INTO tbl_follow(uid1, uid2) VALUES(%s, %s)"
    cursor.execute(sql, [uid1, uid2])

    
    
    h = "<script>alert('Followed Succesfully');window.location='/uvfollow/';</script>"
    return HttpResponse(h)