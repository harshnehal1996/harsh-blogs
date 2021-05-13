from django.http import HttpResponse
from django.shortcuts import redirect

def admin_redirect(view_func):
	def wrapper_function(request, *args, **kwargs):
		if request.user.is_superuser:
			return redirect('adminBlog')
		else:
			return view_func(request, *args, **kwargs)

	return wrapper_function

def admin_only(view_func):
	def wrapper_function(request, *args, **kwargs):
		if request.user.is_superuser:
			return view_func(request, *args, **kwargs)
		else:
			return redirect('home')

	return wrapper_function
