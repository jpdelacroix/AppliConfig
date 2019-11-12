from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

# Create your models here.

class Genre(MPTTModel):
	name = models.CharField(max_length=50, unique=False)
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

	def __str__(self):
		return self.name

	class MPTTMeta:
		order_insertion_by = ['name']

class Vitapi(MPTTModel):
	name = models.CharField(max_length=50, unique=False)
	clef = models.IntegerField(null=True, blank=True,unique=False)
	#ligne = models.IntegerField(null=False, blank=False,unique=True)
	#niveau = models.IntegerField(null=False, blank=False,unique=False)
	parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

	def __str__(self):
		return self.name

	class MPTTMeta:
		order_insertion_by = ['name']		


class Post(models.Model):
	title = models.CharField(max_length=120)
	category = TreeForeignKey('Category',null=True,blank=True, on_delete=models.CASCADE)
	content = models.TextField('Content')
	slug = models.SlugField()

	def __str__(self):
		return self.title

class Category(MPTTModel):
	name = models.CharField(max_length=50, unique=False)
	parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True,on_delete=models.CASCADE)
	slug = models.SlugField()	

	class MPTTMeta:
		order_insertion_by = ['name']

	class Meta:
		unique_together = (('parent', 'slug',))
		verbose_name_plural = 'categories'

	def get_slug_list(self):
		try:
			ancestors = self.get_ancestors(include_self=True)
		except:
			ancestors = []
		else:
			ancestors = [ i.slug for i in ancestors]
		slugs = []
		for i in range(len(ancestors)):
			slugs.append('/'.join(ancestors[:i+1]))
		return slugs

	def __str__(self):
		return self.name

''''
class Company(MPTTModel):
    name = models.CharField(max_length=255)
    parent = TreeForeignKey('self',
                              related_name='client_parent',
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE)
	is_global_ultimate = models.NullBooleanField()
    is_domestic_ultimate = models.NullBooleanField()


    def get_domestic_ultimate(self):

		if self.is_domestic_ultimate:
			return self
		mytree = self.get_ancestors(ascending=True, include_self=False)
		for comp in mytree:
			if comp.is_domestic_ultimate:
			return comp
		return None
'''