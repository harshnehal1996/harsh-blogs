from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from .models import *
from .forms import BlogForm, CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import admin_redirect, admin_only
from newsapi import NewsApiClient
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import BlogSerializer

api_key = '0267638331d64e63b1817ee23318f271'

def registerPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user_email = form.cleaned_data.get('email')
			exists = User.objects.filter(email=user_email).count()
			if not exists:
				form.save()
				user = form.cleaned_data.get('username')
				messages.success(request, 'Account was created for ' + user)
				return redirect('login')
			else:
			    return HttpResponse('Email already registered! please try again')

	context = {'form' : form}
	return render(request, 'dashboard/register.html', context)

def loginPage(request):
	if request.user.is_authenticated:
		return redirect('home')
	else:
		if request.method == 'POST':
			username = request.POST.get('username')
			password = request.POST.get('password')

			user = authenticate(request, username=username, password=password)

			if user is not None:
				login(request, user)
				return redirect('home')
			else:
				messages.info(request, 'Username OR password is incorrect')

		return render(request, 'dashboard/login.html', {})

def logoutPage(request):
	logout(request)
	return redirect('login')

def default(request):
	if request.user.is_authenticated:
		print('authenticated')
		return redirect('home')
	return redirect('login')

# Cant get full detailed user article as you have to pay for it
# found here : https://stackoverflow.com/questions/51984209/how-to-get-full-news-content-from-news-api
# Therefore Redirecting to original article
@login_required(login_url='login')
@admin_redirect
def home(request):
    global api_key
    
    newsapi = NewsApiClient(api_key=api_key)
    top = newsapi.get_top_headlines(sources ='techcrunch')
  
    articles = top['articles']
    desc =[]
    news =[]
    img =[]
    link =[]
  
    for i in range(len(articles)):
        instance = articles[i]
        news.append(instance['title'])
        desc.append(instance['description'])
        img.append(instance['urlToImage'])
        link.append(instance['url'])
    mylist = zip(news, desc, img, link)

    return render(request, 'dashboard/recent_news.html', context ={"mylist":mylist})

@login_required(login_url='login')
@admin_redirect
def list_blog(request):
	user = request.user
	blogs = user.userblog_set.all()

	context = {'blogs':blogs}

	return render(request, 'dashboard/home_page.html', context)

@login_required(login_url='login')
@admin_redirect
def view_blog(request, blog_id):
	try:
		userblog = request.user.userblog_set.get(id=blog_id)
	except:
		return HttpResponse('URL not found!')
	# userblog = UserBlog.objects.get(id=blog_id)
	context = {'userblog' : userblog}
	return render(request, 'dashboard/blog.html', context)

@login_required(login_url='login')
@admin_redirect
def createBlog(request):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		if form.is_valid():
			form.save()
			return redirect('list_blog')
		form.cleaned_data['user'] = request.user
		try:
			form.save()
		except Exception as e:
			return HttpResponse('invalid form. Please try again')
		return redirect('list_blog')

	form = BlogForm(initial={'user':request.user})
	context = {'form':form}
	return render(request, 'dashboard/blogCreatonForm.html', context)

@login_required(login_url='login')
@admin_redirect
def deleteBlog(request, pk):
	try:
		blog = request.user.userblog_set.get(id=pk)
	
		if request.method == 'POST':
			blog.delete()
			return redirect('list_blog')
	except:
		return HttpResponse('Error! Maybe this Blog is not available')

	context = {'item':blog}
	return render(request, 'dashboard/delete.html', context)

@login_required(login_url='login')
@admin_only
@api_view(['GET'])
def adminBlog(request):
	blogs = UserBlog.objects.all().order_by('id')
	serializer = BlogSerializer(blogs, many=True)
	return Response(serializer.data)

@login_required(login_url='login')
@admin_only
@api_view(['POST'])
def adminUpdateBlog(request, blog_id):
	try:
		blog = UserBlog.objects.get(id=blog_id)
		serializer = BlogSerializer(instance=blog, data=request.data)
	except:
		return Response("Error! Maybe this Blog is not available")
	
	if serializer.is_valid():
		serializer.save()
	else:
		return Response("Blog not valid")

	return Response(serializer.data)

@login_required(login_url='login')
@admin_only
@api_view(['POST'])
def adminDeleteBlog(request, blog_id):
	try:
		blog = UserBlog.objects.get(id=blog_id)
		blog.delete()
	except:
		return Response("Error! Maybe this Blog is not available")
	
	return Response("Delete successful")

@login_required(login_url='login')
@admin_only
@api_view(['POST'])
def adminCreateBlog(request):
	serializer = BlogSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()
	else:
		return Response("Blog not valid")
	
	return Response(serializer.data)


