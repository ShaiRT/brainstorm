import brainstorm.reader_drivers as drivers
import pytest
import subprocess

from brainstorm.client import Reader
from brainstorm.client.__main__ import client_cli
from click.testing import CliRunner


class MockDriver():
    def __init__(self, path):
        self._count = 0

    def get_user(self):
        return self.user

    def get_snapshot(self):
        self._count += 1
        return self.snapshot if self._count == 1 else None


@pytest.fixture
def mock_drivers(user, snapshot, monkeypatch):
    MockDriver.user = user
    MockDriver.snapshot = snapshot
    monkeypatch.setitem(drivers,'mock', MockDriver)


def test_attributes(mock_drivers, user):
    reader = Reader('', driver='mock')
    assert reader.user_id == user['user_id']
    assert reader.username == user['username']


def test_iter(mock_drivers, snapshot):
    reader = Reader('', driver='mock')
    assert len(list(iter(reader))) == 1
    reader = Reader('', driver='mock')
    assert next(iter(reader)) == snapshot
'''

def test_cli_missing_argument():
  runner = CliRunner()
  result = runner.invoke(client_cli, ['read'])
  assert 'Missing argument' in result.output


def test_cli_user(mock_drivers, user):
    runner = CliRunner()
    result = runner.invoke(client_cli, ['read','.','-d mock'])
    assert result.exit_code == 0
    assert user['username'] in result.output


def test_cli_snapshot(mock_drivers, snapshot):
    runner = CliRunner()
    result = runner.invoke(client_cli, ['read','.','-d mock'])
    date = snapshot['datetime'].strftime('%B%e, %Y')
    assert result.exit_code == 0
    assert f'Snapshot from {date}' in result.output
'''