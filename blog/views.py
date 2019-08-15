# Create your views here.
from blog.models import Article
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'news.html'


class ArticleView(TemplateView):
    template_name = 'article.html'



# def home(request):
#     post_news = Article.objects.filter(is_active=True)
#     return render(request, 'news.html', locals())
#
# def article(request, article_id):
#     article  = Article.objects.get(id = article_id)
#     return render(request, 'article.html', locals())
#
# def registration(request):
#     return render(request, 'registration.html', locals())