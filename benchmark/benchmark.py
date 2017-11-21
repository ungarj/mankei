#!/usr/bin/env python

import os
import timeit

number = 100
repeat = 3

print "average over %s runs, best of %s" % (number, repeat)

for f in ["gdal_cli.tif", "python.tif", "cython.tif"]:
    if os.path.isfile(f):
        os.remove(f)

# GDAL CLI
command = """
sp = [
    "gdaldem", "hillshade", "test/testdata/6-22-33.tif",
    "gdal_cli.tif", "-compute_edges"
]
process = Popen(sp, stdout=PIPE, stderr=STDOUT)
stdoutdata, stderrdata = process.communicate()
"""
setup = """
from subprocess import Popen, PIPE, STDOUT
"""
print "GDAL CLI: %sms" % (
    min(
        timeit.repeat(command, setup=setup, number=number, repeat=repeat)
    ) * 1000 / number
)

# pure Python/NumPy implementation
command = """
with rasterio.open("test/testdata/6-22-33.tif") as src:
    out_profile = src.meta
    out_profile.update(
        dtype="uint8", nodata=0, transform=out_profile["affine"])
    with rasterio.open("python.tif", "w", **out_profile) as dst:
        dst.write(hillshade(src.read(1), src.affine[0]), 1)
"""
setup = """
import rasterio
from naive_hillshading import hillshade
"""
print "Python:   %sms" % (
    min(
        timeit.repeat(command, setup=setup, number=number, repeat=repeat)
    ) * 1000 / number
)

# Cython
command = """
with rasterio.open("test/testdata/6-22-33.tif") as src:
    out_profile = src.meta
    out_profile.update(
        dtype="uint8", nodata=0, transform=out_profile["affine"])
    with rasterio.open("cython.tif", "w", **out_profile) as dst:
        dst.write(hillshade(src.read(1), src.affine[0]), 1)
"""
setup = """
import rasterio
from mankei import hillshade
"""
print "Cython:   %sms" % (
    min(
        timeit.repeat(command, setup=setup, number=number, repeat=repeat)
    ) * 1000 / number
)
