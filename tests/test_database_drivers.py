import brainstorm.database_drivers as db_drivers
import inspect
import stringcase as sc


def test_import():
    """Test the dynamic importing of the module
    """
    assert type(db_drivers) == dict
    for key, val in db_drivers.items():
        assert inspect.isclass(val)
        assert val.__name__.endswith('Driver')
        assert key + '_driver' == sc.snakecase(val.__name__)
