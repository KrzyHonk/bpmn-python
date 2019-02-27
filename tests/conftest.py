import os

import pytest


@pytest.fixture(scope="module", autouse=True)
def change_path_to_script_location(request):
    test_dir = os.path.dirname(request.module.__file__)
    os.chdir(test_dir)


@pytest.fixture(scope="session", autouse=True)
def reset_path(request):
    initial_dir = os.getcwd()
    yield
    os.chdir(initial_dir)
