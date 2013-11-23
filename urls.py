from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name="login"),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'template_name': 'logout.html'}, name="logout"),

    url(r'^poll/$', 'app.views.poll', name='poll'),
    url(r'^$', 'app.views.index', name='index'),

    url(r'', include('social_auth.urls')),
)
