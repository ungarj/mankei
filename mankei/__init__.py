"""Collection of mankei functions."""


from ._hillshade import _hillshade


def hillshade(
    elevation, resolution, azimuth=315.0, altitude=45.0, z=1.0, scale=1.0
):
    return _hillshade(
        elevation.astype("float"), resolution, azimuth, altitude, z, scale
    ).astype("uint8")
