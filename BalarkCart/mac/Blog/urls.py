from . import views
from django.urls import path

urlpatterns = [
    path("",views.index,name="MyBlog"),
    path("blogpost/<int:id>",views.blogpost,name="BlogPost"),
]