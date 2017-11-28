import os
import rasterio
from glob import glob
import time
import tqdm

from mankei import hillshade

PATH = "/home/ungarj/geodata/cleantopo/mercator_tiled/output/8/"

files = [
    y
    for x in os.walk(PATH)
    for y in glob(os.path.join(x[0], '*.tif'))
]

times = []
for f in tqdm.tqdm(files):
    with rasterio.open(f, "r") as src:
        start = time.time()
        hillshade(src.read(1), src.affine[0])
        times.append(time.time() - start)

print sum(times) / len(times), "s"
