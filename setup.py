# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)

from setuptools import setup

if __name__ == '__main__':

    long_description = open('README').read()

    setup(
        name='gridsup',
        version='0.17',
        description='Database display classes',
        author='Roger Marsh',
        author_email='roger.marsh@solentware.co.uk',
        url='http://www.solentware.co.uk',
        package_dir={'gridsup':''},
        packages=[
            'gridsup',
            'gridsup.core', 'gridsup.gui',
            'gridsup.db', 'gridsup.dpt', 'gridsup.sqlite', 'gridsup.apsw',
            'gridsup.about',
            ],
        package_data={
            'gridsup.about': ['LICENCE', 'CONTACT'],
            },
        long_description=long_description,
        license='BSD',
        classifiers=[
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Operating System :: OS Independent',
            'Topic :: Software Development',
            'Topic :: Database :: Front Ends',
            'Intended Audience :: Developers',
            'Development Status :: 4 - Beta',
            ],
        install_requires=['basesup==0.17'],
        dependency_links=[
            'http://solentware.co.uk/files/basesup-0.17.tar.gz'],
        )
