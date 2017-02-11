# coding: utf-8
from django.shortcuts import render, redirect
from django.http import HttpResponse,HttpResponseRedirect
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth import login, logout, authenticate
import logging
from .models import User,Article,Ad,Comment,Tag,Category
from .forms import CommentForm,ArticleForm 
from django.db.models import Count
from django.core.paginator import Paginator,InvalidPage,EmptyPage,PageNotAnInteger
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import ArticleSerializer 


def global_setting(request):
	comment_count_list = Comment.objects.values('article').annotate(comment_count=Count('article')).order_by('-comment_count')
	article_comment_list = [Article.objects.get(pk=comment['article']) for comment in comment_count_list][:5]
	article_click_list = Article.objects.order_by('click_count')[:5]
	article_recommend_list = Article.objects.filter(is_recommend=True)[:5]
	tags = Tag.objects.all()
	site_name = settings.SITE_NAME
	facebook = settings.FACEBOOK
	distinct_date_list = Article.objects.distinct_date()
	ad_list = Ad.objects.all()
	category_list = Category.objects.all()
	return locals() 


logger = logging.getLogger('logger_test')
# Create your views here.
def paginator_article(request, articles, page, page_data, page_type):
	if page_type=="up":
		page = page-1
	if page_type=="down":
		page = page+1
	paginator = Paginator(articles, page_data)
	try:
		articles = paginator.page(page)
	except (InvalidPage,EmptyPage,PageNotAnInteger) :
		articles = paginator.page(1)
	return {'paginator':paginator, 'articles':articles, 'page':page}

def index(request):

	try:
		
		try:
			page = int(request.GET.get('page', '1'))
			page_type = request.GET.get('page_type')
		except ValueError:
			page = 1
		page_data = 4
		articles = Article.objects.all()
		p_article = paginator_article(request, articles, page, page_data, page_type)			
		paginator = p_article['paginator']
		articles = p_article['articles']
		page = p_article['page']
		
		return render(request, 'index.html', locals())
	except Exception as e:
		logger.error(e)
def archive(request):
	try:
		
		try:
			if request.GET.get('date'):
				date = request.GET.get('date')
				year = date[:4]
				month = date[5:7] 
			else:
				year = request.GET.get('year')
				month = request.GET.get('month')
			page = int(request.GET.get('page', '1'))
			page_type = request.GET.get('page_type')
		except ValueError:
			page = 1
		article_list = Article.objects.filter(date_publish__icontains=year+'-'+month)
		page_data = 4
		p_article = paginator_article(request, article_list, page, page_data, page_type)			
		paginator = p_article['paginator']
		articles = p_article['articles']
		page = p_article['page']

	        
		return render(request, 'index.html', locals())
	except Exception as e:
		logger.error(e)



def reg(request):
	try:
		if request.method=='POST':
			username = request.POST.get("username")	
			email = request.POST.get("email")
			url = request.POST.get("url")
			pwd = request.POST.get("password")
			pwd1 = request.POST.get("password1")
			if pwd == pwd1:
				user = User.objects.create(username=username, email=email, url=url, password=make_password(pwd))	
				user.save()
                                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                                login(request, user)

				return HttpResponse("注册成功")
			else:
				pass
			return redirect('/')
		else:
			return render(request, 'reg.html', locals())
	except Exception as e:
		logger.error(e)

def do_login(request):
        try:
                if request.method=="POST":
                        username = request.POST.get('username') 
                        password = request.POST.get('password')
                        user = authenticate(username=username, password=password)
			
                        if user is not None:
                                user.backend = 'django.contrib.auth.backends.ModelBackend' # 指定默认的登录验证方式
                                login(request, user)
                                return redirect('/')
                        else:
                                return render(request, "failure.html", locals())

        except Exception as e:
                logger.error(e)
        return render(request, 'login.html', locals())

def do_logout(request):
        try:
                logout(request)
        except Exception as e:
                logger.error(e)
        return redirect('/')

def article(request):
	try:
		id = request.GET.get('id')	
		article = Article.objects.get(pk=id)
		article.click_count=article.click_count+1
		article.save()
		
		comments = Comment.objects.filter(article=article).order_by('id') 
		comment_list = []
		for comment in comments:
			for item in comment_list:
				if not hasattr(item, 'children_comment'):
					setattr(item, 'children_comment', [])
				
				if comment.pid == item:
					item.children_comment.append(comment)
			if comment.pid is None:
				comment_list.append(comment)
		return render(request, 'article.html', locals())
	except Exception as e:
		logger.error(e)
def article_update(request, id):
	article = Article.objects.get(pk=id)
	if request.method=='POST':
		article_form = ArticleForm(request.POST,instance=article)
		article_form.save()
		return redirect('/')
	if article.user == request.user:
		article_form = ArticleForm(instance=article)
		tag_id = 3
		flag = 'update'
	else:
		return HttpResponse("修改失败，你无权修改此文章")
	return render(request, 'user.html', locals())

def comment_post(request):
	try:
		if request.method == 'POST':
			comment_form = CommentForm(request.POST)
			comment_form.save()
			article_id = comment_form.cleaned_data['article'].id
			return HttpResponseRedirect('/article?id='+str(article_id))
		else:
			article = Article.objects.get(id=request.GET.get('id'))
			comment_form = CommentForm({'username':request.user.username, 'email':request.user.email, 'url':request.user.url, 'article':article, 'pid':request.GET.get('pid')} if request.user.is_authenticated() else {'article':article})
	
			return render(request, 'comment.html', locals())

	except Exception as e:
		logger.error(e)


def tag_article(request):
	tag_id = request.GET.get('tag_id')
	articles = Article.objects.all()
	article_list = []
	for article in articles:
		tags = article.tag.all()
		for tag in tags:
			if int(tag.id) == int(tag_id):
				article_list.append(article)
	articles = article_list
	try:
		page = int(request.GET.get('page', '1'))
		page_type = request.GET.get('page_type')
	except ValueError:
		page = 1
	page_data = 4
	p_article = paginator_article(request, articles, page, page_data, page_type)	
	paginator = p_article['paginator']
	articles = p_article['articles']
	page = p_article['page']

	
	return render(request, 'index.html', locals())

def user_detail(request):
	try:
		if request.method == 'POST':
			article_form = ArticleForm(request.POST)
			article_form.save()
			tag_id = 2
		else:
			if request.GET.get('tag_id'):
				tag_id = int(request.GET.get('tag_id'))
			else:
				tag_id = 1		
		if tag_id == 2:
			page_data = 4
			articles = Article.objects.filter(user=request.user)
			try:
				page = int(request.GET.get('page', '1'))
				page_type = request.GET.get('page_type')
			except ValueError:
				page = 1
			p_article = paginator_article(request, articles, page, page_data, page_type)	
			paginator = p_article['paginator']
			articles = p_article['articles']
			page = p_article['page']
		if tag_id == 3:
			article = Article.objects.create(user=request.user, content=" ")
			article_form = ArticleForm(instance=article)
	except Exception as e:
		logger.error(e)
	return render(request,'user.html',locals())
	
class ArticleListView(APIView):
	def get(self, request, format=None):
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles, many=True)
		return Response(serializer.data)
	def post(self, request, format=None):
		serializer = ArticleSerializer(data=request.data, many=True)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		else:
			return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def cate_article(request):
	category_id = int(request.GET.get('category_id'))
	category = Category.objects.get(id=category_id)
	articles = Article.objects.filter(category=category) 
	try:
		page = int(request.GET.get('page', '1'))
		page_type = request.GET.get('page_type')
	except ValueError:
		page = 1
	page_data = 2
	p_article = paginator_article(request, articles, page, page_data, page_type)	
	paginator = p_article['paginator']
	articles = p_article['articles']
	page = p_article['page']

	
	return render(request, 'index.html', locals())

def article_delete(request):
	if request.GET.get('id'):
		article_id = int(request.GET.get('id'))
		Article.objects.filter(id=article_id).delete()
		return redirect("/user_detail/?tag_id=2") 
