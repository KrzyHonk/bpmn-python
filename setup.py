# coding=utf-8
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
    version="0.0.19-SNAPSHOT",
    author="Izbela Smietana, Krzysztof Honkisz",
    # author_email = "honkiszkrzystof@gmail.com",
    description=("Python library that allows to import/export BPMN diagram (as an XML file) and provides a simple "
                 "visualization capabilities."),
    license="GNU GENERAL PUBLIC LICENSE",
    keywords=["bpmn", "xml"],
    url="https://github.com/KrzyHonk/bpmn-python",
    download_url="https://github.com/KrzyHonk/bpmn-python/tarball/0.0.19-SNAPSHOT",
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    packages=find_packages(exclude=['docs', 'tests*']),
    install_requires=read('requirements.txt').split('\n'),
    long_description="%s\n%s" % (
        read('README.md'),
        read('CHANGELOG.md')
    ),
    long_description_content_type='text/markdown',
    classifiers=[
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Text Processing :: Markup :: XML"
    ]
)
