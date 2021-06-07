# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

import sys
from distutils.core import setup

from gridsup import _gridsup_version

setup(
    name='-'.join(
        ('gridsup',
         ''.join(
             ('py',
              '.'.join(
                  (str(sys.version_info[0]),
                   str(sys.version_info[1]))))),
         )),
    version=_gridsup_version,
    description='Database display classes',
    author='solentware.co.uk',
    author_email='roger.marsh@solentware.co.uk',
    url='http://www.solentware.co.uk',
    packages=[
        'gridsup',
        'gridsup.core', 'gridsup.gui',
        ],
    package_data={
        'gridsup': ['README', 'LICENCE'],
        },
    long_description='''Database display classes

    Display a scrollable list of records from a database accessed using the
    basesup package.

    Base classes for modifying these records through the basesup package are
    provided.
    ''',
    )
