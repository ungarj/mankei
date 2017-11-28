"""Collection of mankei functions."""


from ._hillshade import _hillshade


def hillshade(
    elevation, resolution, azimuth=315.0, altitude=45.0, z=1.0, scale=1.0
):
    """
    Calculate hillshade from elevation data.

    Parameters
    ----------
    elevation : 2-dimensional array
        Input elevation data.
    resolution : float
        Elevation ground resolution.
    azimuth : float
        Vertical sun angle in degrees. (default: 315)
    altitude : float
        Sun height in degrees. (default: 45)
    z : float
        Vertical elevation exaggeration factor. (default: 1)
    scale : float
        Factor between ground resolution and elevation measurement units. If
        elevation value unit is meter and the ground resolution unit degrees
        (as in e.g. EPSG 4326), the scale factor is recommended to be 112000.
        (default: 1)
    """
    if elevation.ndim != 2:
        raise ValueError("elevation array must be 2-dimensional")
    if not 0 <= azimuth <= 360:
        raise ValueError("azimuth has to be between 0 and 360")
    if not z >= 0:
        raise ValueError("z value has to be greater 0")
    if not scale >= 0:
        raise ValueError("scale has to be greater 0")
    return _hillshade(
        elevation.astype("float"), resolution, azimuth, altitude, z, scale
    ).astype("uint8")
