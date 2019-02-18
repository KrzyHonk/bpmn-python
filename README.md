# bpmn-python
Project for creating a Python library that allows to import/export BPMN diagram (as an XML file) and provides a simple visualization capabilities

Project structure
* bpmn_python - main module of project, includes all source code
* tests - unit tests for package
* examples - examples of XML files used in tests
* docs - documentation for package


## Development

Requirements: [pipenv](https://pipenv.readthedocs.io/en/latest/), Python 3.7. If you do not have Python 3.7 installed, consider using [pyenv](https://github.com/pyenv/pyenv). After setting up, it integrates with pipenv allowing latter to automatically pull correct Python version for use in virtual environment.

To set up local development environment, clone the repository, enter it and execute:
```bash
pipenv install --dev -e .
pipenv shell
```

Run tests with HTML coverage report:
```bash
pytest --cov-report html --cov=bpmn_python
```
