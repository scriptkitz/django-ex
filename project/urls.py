from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from welcome.views import index, health
from welcome.ssr import ssr
#from welcome.subscribe import subscribe
from welcome.weiqi.weiqicmd_views import weiqicmd

urlpatterns = [
    # Examples:
    # url(r'^$', 'project.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', index),
    url(r'^health$', health),
    url(r'^ssr$', ssr),
    #url(r'^subscribe$', subscribe),
    url(r'^weiqicmd$', weiqicmd),
    url(r'^admin/', include(admin.site.urls)),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        url(r'^__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
