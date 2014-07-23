# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

from django.conf.urls import include
from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin

from krwlight import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.HomepageView.as_view()),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^selection/(?P<criterium>[^/]+)/$',
        views.SelectionView.as_view(),
        name='krwlight.selection'),
    )
# TODO: staticfiles
