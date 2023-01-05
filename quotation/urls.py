from django.urls import path

from .views import ( 
	homeview, transpoterview, generalview,
	error_404, add_email, remove_email
	 )

urlpatterns = [
	path('home/', homeview, name='home'),
	path('transpoter/', transpoterview, name='transpoter-home'),
	path('general/', generalview, name='general-home'),
	path('error_404/', error_404, name='error_404'),
	path('addEmail/', add_email, name='add-email'),
	path('remove_email/<int:id>', remove_email, name='remove-email'),

]