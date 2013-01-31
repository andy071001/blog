from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^sblog/', include('sblog.urls')),
	(r'^comments/', include('django.contrib.comments.urls')),
	#(r'^blog/(?P<id>\d+)/commentshow/$', 'blog_show_comment', name='showcomment'),
	#(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/work/blog/static'}),
	# Examples:
    # url(r'^$', 'blog.views.home', name='home'),
    # url(r'^blog/', include('blog.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
	url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)

#urlpatterns += patterns((''),
#	(r'^static/(?P<path>.*)$', 'django.views.static.serve',
#		{'document_root': '/home/blog/static'}
#	)
#)
