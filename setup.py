# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

from distutils.core import setup

from version import _gridsup_version

setup(
    name='gridsup',
    version=_gridsup_version,
    description='Database display classes',
    author='solentware.co.uk',
    author_email='roger.marsh@solentware.co.uk',
    url='http://www.solentware.co.uk',
    package_dir={'gridsup':''},
    packages=[
        'gridsup',
        'gridsup.core', 'gridsup.gui',
        'gridsup.db', 'gridsup.dpt', 'gridsup.sqlite',
        ],
    package_data={
        'gridsup': ['LICENCE'],
        },
    long_description='''Database display classes

    Display a scrollable list of records from a database accessed using the
    basesup package.

    Base classes for modifying these records through the basesup package are
    provided.
    ''',
    )
