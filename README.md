# bpmn-python
Project for creating a Python library that allows to import/export BPMN diagram (as an XML file) and provides a simple visualization capabilities

Project structure
* bpmn_python - main module of project, includes all source code
* tests - unit tests for package
* examples - examples of XML files used in tests
* docs - documentation for package


## Development

Requirements: [pipenv](https://pipenv.readthedocs.io/en/latest/)

To set up local development environment:
```bash
git clone https://github.com/KrzyHonk/bpmn-python
pipenv install --dev -e .
pipenv shell
```

Run tests with HTML coverage report:
```bash
pytest --cov-report html --cov=bpmn_python
```