import os
from setuptools import setup

# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "bpmn_python",
    version = "0.0.1",
    author = "Izbela Smietana, Krzysztof Honkisz",
    #author_email = "honkiszkrzystof@gmail.com",
    description = ("Python library that allows to import/export BPMN diagram (as an XML file) and provides a simple visualization capabilities."),
    license = "GNU GENERAL PUBLIC LICENSE",
    keywords = "bpmn",
    #url = "",
    packages=['bpmn_python'],
    install_requires=[
        'networkx',
        'matplotlib',
    ],
    long_description=read('README.md'),
)

