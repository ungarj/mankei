"""Setup script."""

from setuptools import setup
from distutils.extension import Extension
from Cython.Build import cythonize
import numpy as np

extensions = [
    Extension(
        "mankei._hillshade", ["mankei/_hillshade.pyx"],
        include_dirs=[np.get_include()]
    )
]

setup(
    name='mankei',
    version='0.1',
    description='terrain data processing in cython',
    author='Joachim Ungar',
    author_email='joachim.ungar@gmail.com',
    url='https://github.com/ungarj/mankei',
    license='MIT',
    ext_modules=cythonize(extensions, quiet=True),
    packages=[
        'mankei'
    ],
    install_requires=[
        'Cython',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: GIS',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    setup_requires=['pytest-runner'],
    tests_require=['pytest', 'rasterio']
)
