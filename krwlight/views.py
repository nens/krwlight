# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function

# from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from django.views.generic.base import TemplateView

# from krwlight import models
from krwlight import layouts


ALLOWED_CRITERIA = {'location': 'locatie',
                    'parameter': 'waarnemingssoort/parameter'}


class HomepageView(TemplateView):
    template_name = 'krwlight/homepage.html'
    title = "KRW demo"

    @cached_property
    def layout(self):
        # TODO: Later on, use Reg to get our hands on a layout. Probably by
        # putting some explicit @lizard_layout.view decorator on the class.
        return layouts.BaseLayout(self)


class SelectionView(TemplateView):
    template_name = 'krwlight/selection.html'

    @cached_property
    def title(self):
        return "Selectie op %s - KRW demo" % ALLOWED_CRITERIA[self.criterium]

    @cached_property
    def criterium(self):
        if self.kwargs['criterium'] not in ALLOWED_CRITERIA:
            return
        return self.kwargs['criterium']

    @cached_property
    def layout(self):
        return layouts.BaseLayout(self)
