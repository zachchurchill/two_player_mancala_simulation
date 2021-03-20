import pytest

from mancala.mancala import Player
from mancala.serialize import serialize


def test_serialize_returns_type_error_for_unregistered_type():
    class NewType:
        pass

    with pytest.raises(TypeError):
        serialize(NewType())


@pytest.mark.parametrize(
    "serializable,serialized",
    [
        (Player.ONE, "one"),
        (Player.TWO, "two"),
    ],
)
def test_serialize_returns_correct_serialization(serializable, serialized):
    assert serialize(serializable) == serialized
