
from . import views
from django.urls import path

urlpatterns = [
    path("",views.index,name="ShopeHome"),
    path("contact/",views.contact,name="ContactUs"),
    path("about/",views.about,name="AboutUs"),
    path("tracker/",views.tracker,name="TrackingStatus"),
    path("search/",views.search,name="Search"),
    path("products/<int:myid>",views.productview,name="ProductView"),
    path("checkout/",views.checkout,name="Checkout"),
    path("table/",views.table,name="table"),
    path("table/<int:product_id>/delete",views.deleteProd,name="Delete"),
    path("login/",views.loginPage,name="loginPage"),
    path('register/',views.registerPage,name="registerPage"),
    path('logout/',views.logoutUser,name="logout")

]