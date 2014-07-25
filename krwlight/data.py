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
    tree1 = defaultdict(lambda: defaultdict(list))
    # paramgroup1: paramgroup2: [waarneming, waarneming, waarneming]
    tree2 = []
    # hoedanigheid: [waarneming, waarneming, ...]

    biotaxons = load_csv_data('biotaxon')['biotaxon']
    waarnemingssoorten = load_csv_data('waarnemingsoort')['waarnemingsoort']
    waarnemingen = load_csv_data('waarneming')['waarneming']
    # Note: typo in 'waarnemingsoort' in the csv.

    waarneming_per_waarnemingssoort = defaultdict(list)
    for waarneming in waarnemingen:
        waarneming_per_waarnemingssoort[
            waarneming['Waarnemingssoort']].append(waarneming)
    levels_per_biotaxon = {
        biotaxon['Biotaxon']: (biotaxon['parametergroup1'],
                               biotaxon['parametergroup2'])
        for biotaxon in biotaxons}
    levels_per_waarnemingssoort = {
        waarnemingssoort['Nummer']: levels_per_biotaxon.get(
            waarnemingssoort['Biotaxon'])
        for waarnemingssoort in waarnemingssoorten}

    for waarnemingssoort in waarnemingssoorten:
        id = waarnemingssoort['Nummer']
        # title = waarnemingssoort['Omschrijving']
        title = (waarnemingssoort['Biotaxon'] or
                 waarnemingssoort['Omschrijving'])
        # TODO: biotaxon['localname'] proberen te gebruiken

        num_results = len(waarneming_per_waarnemingssoort[id])
        if not num_results:
            continue
        levels = levels_per_waarnemingssoort[id]
        if levels is not None:
            (level1, level2) = levels
            tree1[level1][level2].append(
                {'id': id,
                 'title': title,
                 'num_results': num_results})
        else:
            tree2.append(
                {'id': id,
                 'title': title,
                 'num_results': num_results})


    tree1 = dict(tree1)
    for k, subtree in tree1.items():
        tree1[k] = dict(subtree)

    result = [
        {'title': 'Biotaxon',
         'children': [
             {'title': title,
              'children': [
                  {'title': title2,
                   'children': children}
                  for title2, children in level2.items()
              ]}
             for title, level2 in tree1.items()
         ]},




        {'title': 'Kwaliteitselementen',
         'children': tree2},
    ]
    return result
