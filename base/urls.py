from django.urls import path
from . import views

urlpatterns = [
    path("", views.home,name="home"),
    path("question/<str:pk>/", views.question,name="question"),
    path("register/", views.registerPage,name="register"),
    path("login/", views.loginPage,name="login"),
    path("logout/",views.logoutPage,name="logout"),
    path("create-post/",views.createPost,name="createpost"),
    path('profile/<str:un>',views.userProfile,name="userprofile"),
    path('update-post/<str:pk>',views.updatePost,name="update-post"),
    path('update-profile/<str:pk>',views.userEdit,name="update-profile"),
    path('delete-post/<str:pk>',views.deletePost,name="delete-post"),
    path('delete-message/<str:pk>/',views.deleteMessage,name="delete-message"),
    path('follow-user/<str:pk>/',views.userFollow,name="follow-user"),
    path('following',views.following,name="following")    

]