# (c) Nelen & Schuurmans.  GPL licensed, see LICENSE.rst.
# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from __future__ import print_function
import csv

# from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.functional import cached_property
from django.views.generic.base import TemplateView

from krwlight import data
from krwlight import layouts


WAARNEMING_FIELDNAMES = ['Waarneming', 'Locatie', 'Datum',
                         'Waarde', 'Activiteit', 'Opmerking',
                         'Waarnemingssoort']
EXTRA_FIELDNAMES_FROM_WAARNEMINGSSOORT = ['Parameter', 'Eenheid',
                                          'Hoedanigheid', 'Biotaxon']
ALLOWED_CRITERIA = {'location': 'locatie',
                    'parameter': 'waarnemingssoort/parameter'}


class HomepageView(TemplateView):
    template_name = 'krwlight/homepage.html'
    title = "HDSR demo"

    @cached_property
    def layout(self):
        # TODO: Later on, use Reg to get our hands on a layout. Probably by
        # putting some explicit @lizard_layout.view decorator on the class.
        return layouts.BaseLayout(self)


class SelectionView(TemplateView):
    template_name = 'krwlight/selection.html'

    @cached_property
    def title(self):
        return "Selectie op %s - HDSR demo" % ALLOWED_CRITERIA[self.criterium]

    @cached_property
    def criterium(self):
        if self.kwargs['criterium'] not in ALLOWED_CRITERIA:
            return
        return self.kwargs['criterium']

    @cached_property
    def layout(self):
        return layouts.BaseLayout(self)

    @cached_property
    def tree(self):
        if self.criterium == 'location':
            return data.location_tree()
        if self.criterium == 'parameter':
            return data.parameter_tree()


class CsvView(TemplateView):
    template_name = 'krwlight/preview.html'
    fields = WAARNEMING_FIELDNAMES + EXTRA_FIELDNAMES_FROM_WAARNEMINGSSOORT

    @cached_property
    def layout(self):
        return layouts.BaseLayout(self)

    @cached_property
    def filter_on(self):
        if 'location' in self.request.GET:
            return 'location'
        if 'parameter' in self.request.GET:
            return 'parameter'

    @cached_property
    def filter_value(self):
        return self.request.GET[self.filter_on]

    def lines(self):
        waarnemingen = data.load_csv_data('waarneming')['waarneming']
        waarnemingssoorten = data.load_csv_data('waarnemingsoort')['waarnemingsoort']
        waarnemingssoorten = {
            waarnemingssoort['Nummer']: waarnemingssoort
            for waarnemingssoort in waarnemingssoorten}
        if self.filter_on == 'location':
            waarnemingen = [waarneming for waarneming in waarnemingen
                            if waarneming['Locatie'] == self.filter_value]
        if self.filter_on == 'parameter':
            waarnemingen = [waarneming for waarneming in waarnemingen
                            if waarneming['Waarnemingssoort'] == self.filter_value]
        for waarneming in waarnemingen:
            waarneming.update(waarnemingssoorten[waarneming['Waarnemingssoort']])
        return waarnemingen

    @cached_property
    def csv_filename(self):
        name = '%s-%s' % (self.filter_on, self.filter_value)
        # Brute force
        name = [char for char in name
                if char in 'abcdefghijklmnopqrstuvwxyz-_ 0123456789']
        name = ''.join(name)
        name = name.replace(' ', '_')
        return name

    @cached_property
    def title(self):
        return self.csv_filename

    def header_line_for_html(self):
        return self.fields

    def lines_for_html(self):
        for line in self.lines():
            yield [line[field] for field in self.fields]


class CsvDownloadView(CsvView):

    def render_to_response(self, context, **response_kwargs):
        """Return a csv response instead of a rendered template."""
        response = HttpResponse(mimetype='text/csv')
        filename = self.csv_filename + '.csv'
        response[
            'Content-Disposition'] = 'attachment; filename="%s"' % filename

        # Ideally, use something like .encode('cp1251') somehow somewhere.
        writer = csv.DictWriter(response,
                                self.fields,
                                delimiter=b';',
                                extrasaction='ignore')
        writer.writeheader()
        for line in self.lines():
            writer.writerow(line)
        return response
