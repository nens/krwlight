# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

# from django.core.urlresolvers import reverse
from django.views.generic.base import TemplateView

# from krwlight import models
from krwlight import layouts


class HomepageView(TemplateView):
    template_name = 'krwlight/homepage.html'

    @property
    def layout(self):
        # TODO: Later on, use Reg to get our hands on a layout. Probably by
        # putting some explicit @lizard_layout.view decorator on the class.
        return layouts.BaseLayout(self)
