from django.shortcuts import render
from blog.models import *
# Create your views here.


def home(request):
	post_news = Article.objects.filter(is_active=True)


	return render(request, 'news.html', locals())




def article(request, article_id):
	article  = Article.objects.get(id = article_id)
	return render(request, 'article.html', locals())



def registration(request):
	return render(request, 'registration.html', locals())