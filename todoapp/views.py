from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Task
from django.contrib.auth.decorators import login_required
from .forms import TaskForm
from datetime import date

User = get_user_model()

def index(request):
    if request.user.is_authenticated:
        task_count = request.user.task_set.filter(due_date=date.today(), completed=False).count()
        context = {
            'task_count': task_count
        }
        return render(request, 'index.html', context)
    return render(request, 'index.html')

def register(request):
    if request.user.is_authenticated is True:
        return redirect(request.META['HTTP_REFERER'])
    if request.method == 'POST':
        username = request.POST['username']
        full_name = request.POST['full_name']
        password = request.POST['password']
        if User.objects.filter(username=username).exists() is True:
            messages.error(request, 'User with username already exists')
            return render(request, 'register.html')
        User.objects.create_user(username=username, password=password, full_name=full_name)
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
    return render(request, 'register.html')

def loginUser(request):
    if request.user.is_authenticated is True:
        return redirect(request.META['HTTP_REFERER'])
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        messages.error(request, 'Invalid Credentials!!!')
    return render(request, 'login.html')

@login_required(login_url='login')
def logoutUser(request):
    logout(request)
    messages.success(request, 'Logged out successful')
    return redirect('index')

@login_required(login_url='login')
def todosList(request):
    todos = request.user.task_set.filter(completed=False).order_by('due_date')
    context = {
        'todos': todos
    }
    return render(request, 'todos.html', context)

@login_required(login_url='login')
def toggleComplete(request, pk):
    task = request.user.task_set.get(pk=pk)
    if task.completed:
        task.completed = False
        task.save()
        return redirect('completed')
    else:
        task.completed = True
        task.save()
        return redirect('view-todos')

@login_required(login_url='login')
def completed(request):
    todos = request.user.task_set.filter(completed=True).order_by('due_date')
    context = {
        'todos': todos
    }
    return render(request, 'completed.html', context)

@login_required(login_url='login')
def detail(request, pk):
    todo = request.user.task_set.get(pk=pk)
    context = {
        'todo': todo
    }
    return render(request, 'detail.html', context)

@login_required(login_url='login')
def createTodo(request):
    form = TaskForm()
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            messages.success(request, 'Task added successfully')
            return redirect('view-todos')
    context = {
        'form': form
    }
    return render(request, 'todo-form.html', context)

@login_required(login_url='login')
def editTodo(request, pk):
    todo = request.user.task_set.get(pk=pk)
    form = TaskForm(instance=todo)
    if request.method == 'POST':
        form = TaskForm(instance=todo, data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Updated task successfully')
            return redirect(f'/todos/{todo.id}/')
    context = {
        'form': form,
        'todo': todo
    }
    return render(request, 'edit-todo.html', context)

@login_required(login_url='login')
def deleteTodo(request, pk):
    todo = request.user.task_set.get(pk=pk)
    todo.delete()
    messages.success(request, 'Task delete successfully')
    return redirect('view-todos')