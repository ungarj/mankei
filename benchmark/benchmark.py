#!/usr/bin/env python

import os
import timeit

number = 10
repeat = 3
testdata = "test/testdata/1024x1024.tif"

print "average over %s runs, best of %s" % (number, repeat)

for f in ["gdal_cli.tif", "python.tif", "cython.tif"]:
    if os.path.isfile(f):
        os.remove(f)

# GDAL CLI
command = """
sp = ["gdaldem", "hillshade", "%s", "gdal_cli.tif", "-compute_edges"]
process = Popen(sp, stdout=PIPE, stderr=STDOUT)
stdoutdata, stderrdata = process.communicate()
""" % testdata
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
with rasterio.open("%s") as src:
    out_profile = src.meta
    out_profile.update(
        dtype="uint8", nodata=0, transform=out_profile["affine"])
    with rasterio.open("python.tif", "w", **out_profile) as dst:
        dst.write(hillshade(src.read(1), src.affine[0]), 1)
""" % testdata
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
with rasterio.open("%s") as src:
    out_profile = src.meta
    out_profile.update(
        dtype="uint8", nodata=0, transform=out_profile["affine"])
    with rasterio.open("cython.tif", "w", **out_profile) as dst:
        dst.write(hillshade(src.read(1), src.affine[0]), 1)
""" % testdata
setup = """
import rasterio
from mankei import hillshade
"""
print "Cython:   %sms" % (
    min(
        timeit.repeat(command, setup=setup, number=number, repeat=repeat)
    ) * 1000 / number
)
