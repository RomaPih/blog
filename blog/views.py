# Create your views here.
from blog.models import Article
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'news.html'


class ArticleView(TemplateView):
    template_name = 'article.html'
