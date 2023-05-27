"""
Test the keygen module.

Author: Alex Wendland
"""
import pytest

from shortener_app.keygen import create_random_generic_key


def test_create_keygen():
    assert len(create_random_generic_key()) == 5
    assert len(create_random_generic_key(10)) == 10
    with pytest.raises(ValueError):
        create_random_generic_key(-10)

    with pytest.raises(ValueError):
        create_random_generic_key(0)
