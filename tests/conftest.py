


import pytest

from emulator_factory import EmulatorFactory



@pytest.fixture(scope="function", autouse=True)
def setup():

    print("Setup for tests")

    emulator_factory = EmulatorFactory()
    emulator_factory.create_emulator('localhost:23')

    yield emulator_factory

    print("Teardown for tests")

    emulator_factory.terminate_emulator()

