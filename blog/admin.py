from django.contrib import admin
from .models import *
# Register your models here.


class ArticleAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Article._meta.fields]
	
	class Meta:
		model = Article

admin.site.register(Article, ArticleAdmin)		 