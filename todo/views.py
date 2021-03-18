from django.shortcuts import render
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


def signup_user(request):
	
	if request.method == 'GET':
		return render(request, 'todo/signup_user.html', {'form': UserCreationForm()})
	else:
		if request.POST['password1'] == request.POST['password2']:
			username = request.POST['username']
			password1 = request.POST['password1']
			user = User.objects.create_user(username, password=password1)
			user.save()
		else:
			print('El password no corresponde')
