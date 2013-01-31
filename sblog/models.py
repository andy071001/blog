from django.db import models

class TestSQL(models.Model):
	test_list = []

class Tag(models.Model):
	"""tag"""
	tag_name = models.CharField(max_length=20, blank=True)
	create_time = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.tag_name

class Author(models.Model):
	"""docstring for Author"""
	name = models.CharField(max_length=30)
	email = models.EmailField(blank=True)
	website = models.URLField(blank=True)

	def __unicode__(self):
		return u"%s" % (self.name)

class Blog(models.Model):
	"""docstring for Blogs"""
	caption = models.CharField(max_length=50)
	author = models.ForeignKey(Author)
	tags = models.ManyToManyField(Tag, blank=True)
	content = models.TextField()
	publish_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)
	taglist = models.CharField(max_length=60,blank=True)
	
	def save(self, *args, **kwargs):
		super(Blog, self).save()
		tagListField = self.taglist.split()
		for i in tagListField:
			p, created = Tag.objects.get_or_create(tag_name=i.strip())
			self.tags.add(p)
	def __unicode__(self):
		return u'%s %s %s' % (self.caption, self.author, self.publish_time)

	class Meta:
		ordering = ['-publish_time']
