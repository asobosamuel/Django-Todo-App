from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('todos/', views.todosList, name='view-todos'),
    path('completed/', views.completed, name='completed'),
    path('todos/<int:pk>/', views.detail, name='detail'),
    path('complete/<int:pk>/', views.toggleComplete, name='toggle-complete'),
    path('create-todo', views.createTodo, name='create-todo'),
    path('edit-todo/<int:pk>/', views.editTodo, name='edit-todo'),
    path('delete-todo/<int:pk>/', views.deleteTodo, name='delete-todo'),
]
