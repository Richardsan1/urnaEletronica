"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from urna import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/<err>', views.login_view_GET),
    path('login/auth/', views.login_view_POST),
    path('register/<err>', views.register_view_GET),
    path('register/save/', views.register_view_POST),
    path('', views.vote_view_GET),
    path('vote/', views.vote_view_POST),
    path('api/candidates/', views.vote_view_GET_candidates),
]
