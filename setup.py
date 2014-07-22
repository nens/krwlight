from setuptools import setup

version = '0.1dev'

long_description = '\n\n'.join([
    open('README.rst').read(),
    open('CREDITS.rst').read(),
    open('CHANGES.rst').read(),
    ])

install_requires = [
    # 'lizard-ui',
    'Django',
    'django-extensions',
    'django-nose',
    'gunicorn',
    'python-memcached',
    'raven',
    'south',
    'werkzeug',
    ],

tests_require = [
    'nose',
    'coverage',
    'mock',
    ]

setup(name='krwlight',
      version=version,
      description="Simple light-weight KRW demo",
      long_description=long_description,
      # Get strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=['Programming Language :: Python',
                   'Framework :: Django',
                   ],
      keywords=[],
      author='Reinout van Rees',
      author_email='reinout.vanrees@nelen-schuurmans.nl',
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
