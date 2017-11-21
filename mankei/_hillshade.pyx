cimport cython
from cython.view cimport array
import numpy as np
cimport numpy as np
from libc.math cimport sin, cos, sqrt, M_PI, atan, atan2
from cython.parallel import prange, parallel

# ctypedef np.uint8_t DTYPE_t
ctypedef np.float64_t DTYPE_t

@cython.boundscheck(False)
@cython.wraparound(False)
@cython.nonecheck(False)
@cython.cdivision(True)
def _hillshade(
    double [:, :] ele,
    float resolution,
    float azimuth,
    float alt,
    float z,
    float scale
):
    cdef:
        unsigned int ncols = ele.shape[1]
        unsigned int nrows = ele.shape[0]
        size_t i, j
        float x = 0.
        float y = 0.
        float slope = 0.
        float aspect = 0.
        float deg2rad = M_PI / 180.
        DTYPE_t [:, :] out = np.empty(shape=(ele.shape[0]-2, ele.shape[1]-2))
        float azimuth_corr = 360 - azimuth + 90

    if (azimuth_corr >= 360.0):
        azimuth_corr = azimuth_corr - 360

    with nogil, parallel(num_threads=4):
        for i in prange(1, ncols - 1):
            for j in range(1, nrows - 1):
                x = (
                    (ele[i, j+1] + 2 * ele[i+1, j] + ele[i+1, j+1]) -
                    (ele[i-1, j-1] + 2 * ele[i-1, j] + ele[i-1, j+1])
                ) / (8 * resolution * scale)
                y = (
                    (ele[i-1, j+1] + 2 * ele[i, j+1] + ele[i+1, j+1]) -
                    (ele[i-1, j-1] + 2 * ele[i, j-1] + ele[i+1, j-1])
                ) / (8 * resolution * scale)
                slope = M_PI/2 - atan(z * sqrt(x*x + y*y))
                aspect = atan2(x, y)
                out[i - 1, j - 1] =  (sin(alt * deg2rad) * sin(slope) \
                    + cos(alt * deg2rad) * cos(slope) \
                    * cos((azimuth_corr - 90.0) * deg2rad - aspect)
                    ) * 255.0  # stretch from 0 to 255 instead of -1 to +1

    return np.pad(np.array(out), 1, mode='edge')
