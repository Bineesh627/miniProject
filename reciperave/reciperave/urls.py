"""reciperave URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from recipeApp.views import *
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

urlpatterns = [
    # Admin pages
    path('admin/', admin.site.urls),
    path('adminhome/', adminhome, name="adminhome"),
    path('viewreg/', viewreg, name="viewreg"),
    path('viewfeedback/', viewfeedback, name="viewfeedback"),
    path('categorys/', categorys, name="categorys"),
    path('categoryForm/', categoryForm, name="categoryForm"),
    path('recipeForm/', recipeForm, name="recipeForm"),
    path('viewrecipe/', viewrecipe, name="viewrecipe"),
    path('deleterecipe/', deleterecipe, name="deleterecipe"),
    path('', index, name="index"),
    # user forms and registration
    path('forgetAction/', forgetAction, name="forgetAction"),
    path('forgetpassword/', forgetpassword, name="forgetpassword"),
    path('profileUpdate/', profileUpdate, name="profileUpdate"),
    path('profileUpdateAction/', profileUpdateAction, name="profileUpdateAction"),
    path('userProfile/', userProfile, name="userProfile"),
    path('newRecipeSearch/', newRecipeSearch, name="newRecipeSearch"),
    path('userRecipeView/', userRecipeView, name="userRecipeView"),
    path('updateRecipeAction/', updateRecipeAction, name="updateRecipeAction"),
    path('updaterecipe/', updaterecipe, name="updaterecipe"),
    path('registerForm/', registerForm, name="registerForm"),
    path('userLogin/', userLogin, name="userLogin"),
    path('feedbackForm/', feedbackForm, name="feedbackForm"),
    path('uploadForm/', uploadForm, name="uploadForm"),
    path('uploadnForm/', uploadnForm, name="uploadnForm"),
    path('feedback/', feedback, name="feedback"),
    path('userhome/', userhome, name="userhome"),
    path('index/', index, name="index"),
    path('upload/', upload, name="upload"),
    path('uploadn/', uploadn, name="uploadn"),
    path('login/', login, name="login"),
    path('register/', register, name="register"),
    path('updaten/', updaten, name="updaten"),
    path('updatenAction/', updatenAction, name="updatenAction"),
    path('deleten/', deleten, name="deleten"),
    path('viewprof/', viewprof, name="viewprof"),
    path('followUser/', followUser, name="followUser"),
    path('uvfollow/', uvfollow, name="uvfollow"),
    path('followBackUser/', followBackUser, name="followBackUser"),
    path('textrec/', textrec, name="textrec"),
    path('TrecipeSearch/', TrecipeSearch, name="TrecipeSearch"),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += staticfiles_urlpatterns()