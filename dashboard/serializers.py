from rest_framework import serializers
from .models import UserBlog

class BlogSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserBlog
		fields ='__all__'
