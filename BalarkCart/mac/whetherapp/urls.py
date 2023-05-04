from django.urls import path
from . import views

urlpatterns = [
    path('',views.whetherPage,name="Weather")
]
