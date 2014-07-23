# File for data imports from csv.
# Quick&dirty.
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
    """Return nested list with id/name pairs of locations"""
    locations = load_csv_data('locaties')['locaties']
    waarnemingen = load_csv_data('waarneming')['waarneming']
    krw = {'id': 'KRW',
           'title': 'KRW locaties',
           'children': []}
    meetnet = {'id': 'MEETNET',
               'title': 'Roulerend meetnet locaties',
               'children': []}
    project = {'id': 'PROJECT',
               'title': 'Projectlocaties',
               'children': []}
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
        if not (location['KRW_Waterlichaam'] or
                location['Roulerend_Meetnet']):
            project['children'].append(node)
    return [krw, meetnet, project]


# def location_tree():
#     """Return nested list with id/name pairs of locations"""
#     locations = load_csv_data('locaties')['locaties']
#     krw = {'id': 'KRW',
#            'title': 'KRW locaties',
#            'has_children': True,
#            'level': 1,
#            'children': []}
#     meetnet = {'id': 'MEETNET',
#                'title': 'Roulerend meetnet locaties',
#                'has_children': True,
#                'level': 1,
#                'children': []}
#     project = {'id': 'PROJECT',
#                'title': 'Projectlocaties',
#                'has_children': True,
#                'level': 1,
#                'children': []}
#     for location in locations:
#         id = location['LOC_NAME']
#         title = location['Locatiebeschrijving'] or id
#         node = {'id': id,
#                 'title': title,
#                 'has_children': False,
#                 'level': 2,
#                 'children': []}
#         if location['KRW_Waterlichaam']:
#             krw['children'].append(node)
#         if location['Roulerend_Meetnet']:
#             meetnet['children'].append(node)
#         if not (location['KRW_Waterlichaam'] or
#                 location['Roulerend_Meetnet']):
#             project['children'].append(node)
#     result = {'id': 'ROOT',
#               'title': 'Alle locaties',
#               'has_children': True,
#               'level': 0,
#               'children': [krw, meetnet, project]}
#     return result
