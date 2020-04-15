import brainstorm.parsers as parsers
import inspect
import json
import pytest
import stringcase as sc

from brainstorm.parsers.__main__ import parsers_cli
from click.testing import CliRunner



def test_import():
    """Test the dynamic importing of the module
    """
    assert type(parsers.parsers) == dict
    for key, val in parsers.parsers.items():
        assert inspect.isclass(val) or inspect.isfunction(val)
        if inspect.isclass(val):
            assert val.__name__.endswith('Parser')
            assert key + '_driver' == sc.snakecase(val.__name__)
        else:
            assert val.__name__.startswith('parse')
            assert 'parse_' + key == val.__name__


def test_feelings_parser(snapshot_no_blobs, user):
    snapshot = snapshot_no_blobs
    snapshot['user'] = user
    result = parsers.parsers['feelings'](snapshot)
    assert set(result.keys()) == set(['feelings', 'datetime', 'user'])


def test_pose_parser(snapshot_no_blobs, user):
    snapshot = snapshot_no_blobs
    snapshot['user'] = user
    result = parsers.parsers['pose'](snapshot)
    assert set(result.keys()) == set(['pose', 'datetime', 'user'])


def test_color_image_parser(snapshot, user, tmp_path):
    snapshot['user'] = user
    (tmp_path / 'color_image').write_bytes(snapshot['color_image']['data'])
    snapshot['color_image']['path'] = str(tmp_path / 'color_image')
    del snapshot['color_image']['data']
    result = parsers.parsers['color_image'](snapshot)
    assert set(result.keys()) == set(['color_image', 'datetime', 'user'])
    assert (tmp_path / 'color_image.png').exists()


def test_depth_image_parser(snapshot, user, tmp_path):
    snapshot['user'] = user
    (tmp_path / 'depth_image').write_bytes(snapshot['depth_image']['data'])
    snapshot['depth_image']['path'] = str(tmp_path / 'depth_image')
    del snapshot['depth_image']['data']
    result = parsers.parsers['depth_image'](snapshot)
    assert set(result.keys()) == set(['depth_image', 'datetime', 'user'])
    assert (tmp_path / 'depth_image.png').exists()


@pytest.fixture
def mock_my_parser(monkeypatch):
    def my_parser(data):
        print('this is my parser')
        return data
    monkeypatch.setitem(parsers.parsers, 'my_parser', my_parser)


def test_parse_fail(mock_my_parser):
    result = parsers.parse('not_a_parser', json.dumps({'a': 1}))
    assert result == None
    result = parsers.parse('my_parser', json.dumps({'a': 1}))
    assert result == None


def test_parse_path(mock_my_parser, tmp_path):
    path = tmp_path / 'data.txt'
    path.write_text(json.dumps({'my_parser': 1}))
    result = parsers.parse_path('my_parser', str(path))
    assert result == json.dumps({'my_parser': 1})


def test_cli_parse_missing_argument():
    runner = CliRunner()
    result = runner.invoke(parsers_cli, ['parse'])
    assert 'Missing argument' in result.output


# TODO: add message queue and cli testing

