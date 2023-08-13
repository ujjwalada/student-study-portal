"""My URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
import imp
from re import template
from django import views
from django.contrib import admin
from django.urls import path


from app01 import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    path('notes', views.notes, name="notes"),
    path('delete_notes/<int:pk>', views.delete_note, name="delete_notes"),
    path('detail/<int:detail_id>', views.detail, name="detail"),
    path('homework', views.homwork, name="homework"),
    path('update_homework/<int:pk>', views.update_homework, name="update-homewok"),
    path('delete_homework/<int:pk>', views.delete_homework, name="delete_homework"),
    path('youtube', views.youtube, name="youtube"),
    path('todo', views.todo, name="todo"),
    path('update_todo/<int:pk>', views.update_todo, name="update-todo"),
    path('delete_todo/<int:pk>', views.delete_todo, name="delete_todo"),
    path('book', views.book, name="book"),
    path('dict', views.dict, name='dict'),
    path('wiki', views.wiki, name='wiki'),
    path('register/', views.register, name='register'),
    path('login/', auth_view.LoginView.as_view(template_name="dashboard/login.html"), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name="dashboard/logout.html"), name='logout')


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
