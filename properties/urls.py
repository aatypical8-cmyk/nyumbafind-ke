from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    path('post-property/', views.post_property, name='post_property'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my-properties/', views.my_properties, name='my_properties'),
    path('edit-property/<int:pk>/', views.edit_property, name='edit_property'),
        path('delete-property/<int:pk>/', views.delete_property, name='delete_property'),
    path('profile/', views.profile, name='profile'),
]
