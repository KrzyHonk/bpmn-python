#coding=utf-8
import os

from setuptools import setup, find_packages


def read(fname):
    """
    Utility function to read the README file. Used for the long_description.
    :param fname:
    :return:
    """
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="bpmn_python",
    version="0.0.12",
    author="Izbela Smietana, Krzysztof Honkisz",
    # author_email = "honkiszkrzystof@gmail.com",
    description=("Python library that allows to import/export BPMN diagram (as an XML file) and provides a simple "
                 "visualization capabilities."),
    license="GNU GENERAL PUBLIC LICENSE",
    keywords=["bpmn", "xml"],
    url="https://github.com/KrzyHonk/bpmn-python",
    download_url="https://github.com/KrzyHonk/bpmn-python/tarball/0.0.12",
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=[
        'networkx',
        'matplotlib',
        'pydotplus',
    ],
    long_description=read('README.md'),
)
