from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as authentication
from . import views

urlpatterns = [
	path('', views.default, name="default"),
	path('register/', views.registerPage, name="register"),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutPage, name="logout"),
    path('home/', views.home, name="home"),
    path('view_blog/<str:blog_id>/', views.view_blog, name="view_blog"),
    path('createBlog/', views.createBlog, name="createBlog"),
    path('delete_blog/<str:pk>/', views.deleteBlog, name="delete_blog"),
    path('list_blog/', views.list_blog, name="list_blog"),
    path('adminBlog/', views.adminBlog, name="adminBlog"),
    path('adminUpdateBlog/<str:blog_id>/', views.adminUpdateBlog, name="adminUpdateBlog"),
    path('adminDeleteBlog/<str:blog_id>/', views.adminDeleteBlog, name="adminDeleteBlog"),
    path('adminCreateBlog/', views.adminCreateBlog, name="adminCreateBlog"),
    path('reset_password/', authentication.PasswordResetView.as_view(template_name='dashboard/reset_pwd.html'), name="reset_password"),
    path('password_reset_done/', authentication.PasswordResetDoneView.as_view(template_name='dashboard/password_sent.html'), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/', authentication.PasswordResetConfirmView.as_view(template_name='dashboard/password_reset_confirm.html'), name="password_reset_confirm"),
    path('password_reset_complete/', authentication.PasswordResetCompleteView.as_view(template_name='dashboard/reset_complete.html'), name="password_reset_complete"),
]
