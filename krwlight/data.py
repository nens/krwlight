# File for data imports from csv.
# Quick&dirty.
from collections import defaultdict
import glob
import logging
import os
import csv

from django.conf import settings

logger = logging.getLogger(__name__)


def load_csv_data(limit_to=None):
    """Return dict with csv filenames and their data."""
    pattern = os.path.join(settings.CSV_ROOT, '*.csv')
    result = {}
    for csv_filepath in glob.glob(pattern):
        filename = os.path.basename(csv_filepath).split('.')[0].lower()
        if limit_to is not None:
            if limit_to != filename:
                logger.debug("Skipping %s", filename)
                continue
        logger.debug("Importing %s", filename)
        reader = csv.DictReader(open(csv_filepath), delimiter=';')
        # print reader.fieldnames
        lines = list(reader)
        result[filename] = lines
    return result


def location_tree():
    locations = load_csv_data('locaties')['locaties']
    waarnemingen = load_csv_data('waarneming')['waarneming']
    krw = {'id': 'KRW',
           'title': 'KRW locaties',
           'children': []}
    meetnet = {'id': 'MEETNET',
               'title': 'Roulerend meetnet locaties',
               'children': []}
    # project = {'id': 'PROJECT',
    #            'title': 'Projectlocaties',
    #            'children': []}
    for location in locations:
        id = location['LOC_NAME']
        if not id:
            continue
        title = location['Locatiebeschrijving'] or id
        num_results = len(
            [waarneming for waarneming in waarnemingen
             if waarneming['Locatie'] == id])
        node = {'id': id,
                'title': title,
                'num_results': num_results,
                'children': []}
        if location['KRW_Waterlichaam']:
            krw['children'].append(node)
        if location['Roulerend_Meetnet']:
            meetnet['children'].append(node)
        # if not (location['KRW_Waterlichaam'] or
        #         location['Roulerend_Meetnet']):
        #     project['children'].append(node)
    return [krw, meetnet]


def parameter_tree():
    waarnemingssoorten = load_csv_data('waarnemingsoort')['waarnemingsoort']
    # Note: typo in 'waarnemingsoort' in the csv.

    waarnemingssoort_per_biotaxon = defaultdict(list)
    for waarnemingssoort in waarnemingssoorten:
        waarnemingssoort_per_biotaxon[
            waarnemingssoort['Biotaxon']].append(waarnemingssoort)

    biotaxons = load_csv_data('biotaxon')['biotaxon']
    parents = defaultdict(list)
    for biotaxon in biotaxons:
        id = biotaxon['Biotaxon']
        parents[biotaxon['parentname']].append(id)

    def children(id):
        child_list = []
        parent = parents[id]
        for child_id in parent:
            child = {'id': child_id,
                     'children': children(child_id)}
            child_list.append(child)
        return child_list

    result = {'id': '',
              'children': children('')}
    logger.debug("Calculated it all")


    # waarnemingen = load_csv_data('waarneming')['waarneming']
    return dict(result)
