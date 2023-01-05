from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages

from .forms import CustomUserCreationForm

# class SignUpView(LoginRequiredMixin, CreateView):
# 	# def get(self, request):
# 	# 	print(f"request data : {request.user.acc_type}")
# 	# 	if request.user.acc_type != "AD":
# 	# 		return redirect('login')

# 	form_class = CustomUserCreationForm
# 	success_url = reverse_lazy('general-home')
# 	template_name = 'registration/signup.html'

# 	# def get(self, request):
# 	# 	print(f"request data : {request.user.acc_type}")
# 	# 	if request.user.acc_type != "AD":
# 	# 		return redirect('login')
		
@login_required
def signup(request):
	if str(request.user) == "AnonymousUser":
		return redirect('login')
	elif request.user.acc_type != "AD":
		return redirect('login')

	form = CustomUserCreationForm(request.POST or None)

	if form.is_valid():
		form.save()
		msg = f"{form.cleaned_data.get('username')} Account Created Successfully..."
		messages.add_message(request, messages.INFO, msg)
		return redirect('signup')

	data = {'form': form}

	return render(request, 'registration/signup.html', data)


class UserLoginView(LoginView):
	template_name = 'registration/login.html'
