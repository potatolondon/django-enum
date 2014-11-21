import os
from setuptools import setup

NAME = 'django-enum'
MODULES = ['enum']

DESCRIPTION = 'An Enum helper class for defining choices for Django model and form fields'
URL = "https://github.com/potatolondon/django-enum"

LONG_DESCRIPTION = open(os.path.join(os.path.dirname(__file__), 'README.md')).read()
AUTHOR = 'Potato London Ltd.'

setup(
    name=NAME,
    version='1.0',
    py_modules=MODULES,

    # metadata for upload to PyPI
    author=AUTHOR,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    keywords=(
        "python", "enum", "django", "utility"
    ),
    url=URL
)
