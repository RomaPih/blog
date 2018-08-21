from django.db import models

# Create your models here.
class Article(models.Model):
	title = models.CharField(max_length=120)
	post = models.TextField()
	image = models.ImageField(upload_to='img/')
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	update = models.DateTimeField(auto_now_add=False, auto_now=True)


	def  __str__(self):
		return  "  %s" % self.id

	class Meta:
		verbose_name='Стаття'
		verbose_name_plural= 'Статті'	