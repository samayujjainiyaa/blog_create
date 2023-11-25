from django.urls import path,include
from . import views 

urlpatterns =[
    path('',views.index),
    path('signup/',views.signup, name ="signup"),
    path('ulogin/',views.mainlogin, name="ulogin"),
    path('logout',views.logout),
    path('personal',views.personal),
    path('blog/',views.blog, name="blog"),
    ]

