"""Tests for module."""

import numpy as np
import numpy.ma as ma

from mankei import hillshade


def test_array_output():
    """Test NumPy array and masked array output."""
    test_shape = (256, 256)

    # np.ndarray
    test_data = np.ones(test_shape)
    output = hillshade(test_data)
    assert isinstance(output, np.ndarray)
    assert output.shape == test_shape
    assert not isinstance(output, ma.masked_array)

    # ma.masked_array
    test_data = ma.masked_array(data=np.ones(test_shape))
    output = hillshade(test_data)
    assert isinstance(output, ma.masked_array)
    assert output.shape == test_shape
