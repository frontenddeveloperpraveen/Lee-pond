# Django-Imports
from django.urls import path
from . import views 


urlpatterns = [
    path('login/', views.Login, name='login'),
    path('api/login', views.Login_Submit, name='login api'),
    path('', views.Page1, name='status_screen'),
    path('home', views.Home, name='Home'),



    # Our
    path('logout/', views.Logout.as_view(), name='logout'),
    path("api/submit",views.Form_Submit,name="Form Submit"),
    path('media/<path:file_path>/', views.Media_Download, name='serve_file'),
    path("password-reset/",views.Forget_Password ,name='Password reset'),
    path('password-reset-confirm/<uidb64>/<token>/', views.Reset_Password_Link ,name='password_reset_confirm'),
    

# AJAX APS

    path("api/get/base",views.Base_Page,name="BASE"),
    path("api/get/addr/notifications",views.Notification_api,name="Notification_API"),
    path("api/get/addr/home",views.Home_api,name="Home_API"),
    path("api/get/addr/profile",views.Profile_api,name="Profile_API"),
    path("api/get/addr/orders",views.Orders_api,name="Profile_API"),

#AJAX SUB Order APIS

    path("api/get/state/<route>",views.Order_switch,name="Past_Order_API"),

    path("api/get/addr/perticular/order/<str:param>",views.Perticular_Order,name="Order_Perticular_API"),


#Activity status

    path("api/userstate/<str:state>",views.UserActivity,name="User__Activity")

]


