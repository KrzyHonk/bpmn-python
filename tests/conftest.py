import os
import sys
import pytest


@pytest.fixture(scope="module", autouse=True)
def execute_before_any_test():
    os.chdir(sys.path[0])
