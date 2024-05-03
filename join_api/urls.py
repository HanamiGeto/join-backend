"""join_api URL Configuration

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
from django.urls import path, include
from join.views import CategoryDetail, CategoryList, ContactDetail, ContactList, LoginView, SubtaskDetail, SubtaskList, TaskList, TaskDetail, RegistrationView
from rest_framework import routers
from join import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('tasks/', TaskList.as_view()),
    path('tasks/<int:pk>/', TaskDetail.as_view()),
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>/', CategoryDetail.as_view()),
    path('subtask/', SubtaskList.as_view()),
    path('subtask/<int:pk>/', SubtaskDetail.as_view()),
    path('contact/', ContactList.as_view()),
    path('contact/<int:pk>/', ContactDetail.as_view()),
]
