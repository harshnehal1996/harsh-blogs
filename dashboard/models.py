from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# class User(models.Model):
# 	name = models.CharField(max_length=200)
# 	phone = models.CharField(max_length=200, null=True)
# 	email = models.CharField(max_length=200, null=True)
# 	date_joined = models.DateTimeField(auto_now_add=True, null=True)

# 	def __str__(self):
# 		return self.name

class UserBlog(models.Model):
	blog_tittle = models.CharField(max_length=200)
	user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
	text = models.TextField(null=True, blank=True)
	date_created = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.blog_tittle
