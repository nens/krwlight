KRW "light", simple demo
==========================================

Introduction

Usage, etc.


TODO: before releasing the site, adjust ``fabfile.cfg`` to point at the
correct server and configure raven/sentry and gaug.es in the django settings.


Initial setup
--------------------------------

Initially, there's no ``buildout.cfg``. You need to make that a symlink to the
correct configuration. On your development machine, that is
``development.cfg`` (and ``staging.cfg`` or ``production.cfg``, for instance
on the server)::

    $ ln -s development.cfg buildout.cfg

Then run bootstrap and buildout, as usual::

    $ python bootstrap.py
    $ bin/buildout

Set up a database (and yes, set up an admin user when asked)::

    $ bin/django syncdb
    $ bin/django migrate

And import two fixtures. The background_maps sets up a couple of lizard-map
defaults. Democontent gives you an initial homepage and a link to an example
WMS layer::

    $ bin/django loaddata background_maps
    $ bin/django loaddata democontent

Start the server::

    $ bin/django runserver
