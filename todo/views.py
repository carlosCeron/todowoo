from django.db import IntegrityError
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo


def home(request):
	return render(request, 'todo/home.html')


def login_user(request):
	login_error = 'Autenticacion fallida!'
	if request.method == 'GET':
		return render(request, 'todo/signup_user.html', {'form': AuthenticationForm()})
	else:
		user = authenticate(request, username=request.POST['username'],password=request.POST['password'])
		if user is None:
			return render(request, 'todo/signup_user.html', {'form': AuthenticationForm(), 'error': login_error})
		else:
			login(request, user)
			return redirect('current_todos')
	

def signup_user(request):
	msg_integrity = 'Error con nombre de usuario repetido'
	msg_password_error = 'Password no son iguales'
	if request.method == 'GET':
		return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			try:
				username = request.POST['username']
				password1 = request.POST['password1']
				user = User.objects.create_user(username, password=password1)
				user.save()
				login(request, user)
				return redirect('current_todos')
			except IntegrityError:
				return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': msg_integrity})
		else:
			return render(request, 'todo/signup_user.html', {'form': UserCreationForm(), 'error': msg_password_error})


def current_todos(request):
	todos = Todo.objects.filter(user=request.user, date_completed__isnull=True)
	return render(request, 'todo/current_todos.html', {'todos': todos})


def logout_user(request):
	if request.method == 'POST':
		logout(request)
		return redirect('home')


def create_todo(request):
	if request.method == 'GET':
		return render(request, 'todo/create_todo.html', {'form': TodoForm()})
	else:
		try:
			form = TodoForm(request.POST)
			new_todo = form.save(commit=False)  # Crea el objeto pero no guarda.
			new_todo.user = request.user  # asigna el usuario y espera para guardar en la siguiente linea
			new_todo.save()  # guarda el objeto Todo con el usuario creado.
		except ValueError:
			return render(request, 'todo/create_todo.html', {'form': TodoForm(), 'error': 'Bad Data'})
		return redirect('current_todos')

