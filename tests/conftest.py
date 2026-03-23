import copy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def reset_activities_state():
    # Snapshot/restore the mutable global state to keep tests independent.
    original = copy.deepcopy(activities)
    yield
    activities.clear()
    activities.update(original)


@pytest.fixture
def client(reset_activities_state):
    return TestClient(app)
