from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('module/<slug:module_slug>/', views.module_page, name='module_page'),
    path('logout/', views.logout_view, name='logout'),
]
