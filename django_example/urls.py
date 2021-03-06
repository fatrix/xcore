from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', direct_to_template, {'template': 'index.html'}),
    (r'^admin/', include(admin.site.urls)),

)  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
