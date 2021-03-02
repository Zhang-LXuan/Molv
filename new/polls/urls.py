from django.urls import path

from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.HomeView, name='home'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]
