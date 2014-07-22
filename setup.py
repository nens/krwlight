from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    'Django',
    'django-celery',
    'django-extensions',
    'django-nose',
    'gunicorn',
    'lizard-map',
    'lizard-ui',
    'python-memcached',
    'raven',
    'werkzeug',
    # Maptree and wms are included for demo purposes; almost every site needs
    # them anyway.
    'lizard-maptree',
    'lizard-wms',
    ],

tests_require = [
    'nose',
    'coverage',
    'mock',
    ]

setup(name='krwlight',
      version=version,
      description="TODO",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='TODO',
      author_email='TODO@nelen-schuurmans.nl',
      url='',
      license='GPL',
      packages=['krwlight'],
      include_package_data=True,
      zip_safe=False,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require={'test': tests_require},
      entry_points={
          'console_scripts': [
          ]},
      )
