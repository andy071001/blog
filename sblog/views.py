from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response
from sblog.models import Blog, Author, Tag
from sblog.forms import BlogForm, TagForm

def blog_show_comment(request, id=''):
	blog = Blog.objects.get(id=id)
	return render_to_response('blog_comments_show.html', {"blog": blog})

def blog_search(request):
	tags = Tag.object.all()
	if 'search' in request.GET:
		search = request.GET['search']
		blogs = Blog.objects.filter(caption__icontains=search)
		return render_to_response('blog_filter.html', {"blogs": blogs, "tags": tags}, context_instance=RequestContext(request))
	else:
		blogs = Blog.objects.order_by('-id')
		return render_to_response("blog_list.html", {"blogs": blogs, "tags": tags}, context_instance=RequestContext(request))


def blog_del(request, id=""):
	try:
		blog = Blog.objects.get(id=id)
	except Exception:
		raise Http404
	if blog:
		blog.delete()
		return HttpResponseRedirect("/sblog/bloglist/")
	blogs = Blog.objects.all()
	return render_to_response("blog_list.html", {"blogs": blogs})


def blog_update(request, id=""):
	id = id
	if request.method == 'POST':
		form = BlogForm(request.POST)
		tag = TagForm(request.POST)
		if form.is_valid() and tag.is_valid():
			cd = form.cleaned_data
			cdtag = tag.cleaned_data
			tagname = cdtag['tag_name']
			tagnamelist = tagname.split()
			
			#return HttpResponse('testforfun')

			title = cd['caption']
			content = cd['content']
			blog = Blog.objects.get(id=id)
			if blog:
				blog.caption = title
				blog.content = content
				blog.taglist = tagname
				blog.save()
				tags = blog.tags.all()
				for name in tags:
					name = unicode(str(name), "utf-8")
					if name not in tagnamelist:
						notag = blog.tags.get(tag_name=name)
						blog.tags.remove(notag)
			else:
				blog = Blog(caption=title, content=content)
				blog.save()
			return HttpResponseRedirect('/sblog/blog/%s' % id)
	else:
		try:
			blog = Blog.objects.get(id=id)
		except Exception:
			raise Http404
		form = BlogForm(initial={'caption':blog.caption, 'content':blog.content}, auto_id=False)
		tags = blog.tags.all()
		if tags:
			taginit = ''
			for x in tags:
				taginit += str(x) + ' '
			tag = TagForm(initial={'tag_name': taginit})
		else:
			tag = TagForm()
	return render_to_response('blog_add.html', {'blog': blog, 'form': form, 'id': id, 'tag': tag}, context_instance=RequestContext(request))

def blog_add(request):
	if request.method == 'POST':
		form = BlogForm(request.POST)
		tag = TagForm(request.POST)
		if form.is_valid() and tag.is_valid():
			cd = form.cleaned_data
			cdtag = tag.cleaned_data
			tagname = cdtag['tag_name']
			
			#for taglist in tagname.split():
			#	Tag.objects.get_or_create(tag_name=taglist.strip())
			title = cd['caption']
			author = Author.objects.get(id=1)
			content = cd['content']
			blog = Blog(caption=title, author=author, content=content, taglist=tagname)
			blog.save()

			#for taglist in tagname.split():
			#	blog.tags_set.add(Tag.objects.get(tag_name=taglist.strip())
			#	blog.save()

			id = Blog.objects.order_by('-publish_time')[0].id
			return HttpResponseRedirect('/sblog/blog/%s' % id)
	else:
		form = BlogForm()
		tag = TagForm(initial={'tag_name': 'notags'})
#	return render_to_response('blog_add.html', {'form': form}, context_instance=RequestContext(request))
	return render_to_response('blog_add.html', {'form': form, 'tag': tag}, context_instance=RequestContext(request))

def blog_list(request):
	blogs = Blog.objects.all()
	return render_to_response("blog_list.html", {"blogs":blogs})

def blog_show(request, id=''):
	try:
		blog = Blog.objects.get(id=id)
	except:
		raise Http404
	return render_to_response("blog_show.html", {"blog": blog}, context_instance=RequestContext(request))
