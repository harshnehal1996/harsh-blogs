from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserBlog
from django import forms


class BlogForm(ModelForm):
	def save(self):
		data = self.cleaned_data
		blog = UserBlog(blog_tittle=data['blog_tittle'], user=data['user'],
        				text=data['text'])
		blog.save()
		return blog

	class Meta:
		model = UserBlog
		fields = '__all__'


class CreateUserForm(UserCreationForm):

	email = forms.CharField(max_length=75, required=True)
	
	class  Meta(object):
		model = User
		fields = ['username', 'email', 'password1', 'password2']