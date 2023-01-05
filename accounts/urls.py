from django.urls import path

from .views import signup, UserLoginView
from .forms import CustomLoginForm

urlpatterns = [
	path('signup/', signup, name='signup'),
	path('login/', UserLoginView.as_view(authentication_form=CustomLoginForm), name='login'),

]