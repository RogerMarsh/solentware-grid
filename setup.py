# setup.py
# Copyright 2011 Roger Marsh
# Licence: See LICENCE (BSD licence)
"""solentware-grid setup file."""

from setuptools import setup

if __name__ == "__main__":

    long_description = open("README").read()

    setup(
        name="solentware-grid",
        version="2.1.3",
        description="Database display classes",
        author="Roger Marsh",
        author_email="roger.marsh@solentware.co.uk",
        url="http://www.solentware.co.uk",
        packages=[
            "solentware_grid",
            "solentware_grid.core",
            "solentware_grid.gui",
            "solentware_grid.dpt",
        ],
        long_description=long_description,
        license="BSD",
        classifiers=[
            "License :: OSI Approved :: BSD License",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: OS Independent",
            "Topic :: Software Development",
            "Topic :: Database :: Front-Ends",
            "Intended Audience :: Developers",
            "Development Status :: 3 - Alpha",
        ],
    )
