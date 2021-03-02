from django.contrib import admin
from django.urls import path,include
from . import views

app_name = "login1"
urlpatterns = [
    
    path('index/', views.index,name='index'),
    path('login/', views.login,name='login'),
    path('register/', views.register,name='register'),
    path('logout/', views.logout,name='logout'),
    
    path('shop/', views.shop,name='shop'),
    path('item/<int:item_idd>', views.item,name='item'),
    path('watch/',views.watch,name='watch'),
    path('buy/<int:item_id1>',views.buy,name='buy'),
    path('getcar/',views.getcar,name="getcar"),
    path('reducar/<int:item_id2>',views.reducar,name='reduce'),
    path('submit/',views.submit,name='submit'),
]