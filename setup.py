from setuptools import setup, find_packages, Extension
from codecs import open
from os import path
from Cython.Build import cythonize
from Cython.Distutils import build_ext

here = path.abspath(path.dirname(__file__))

setup(
    name='audiopy',
    version='0.1.dev1',
    description='Audio tools for Python',
    url='https://github.com/aszkid/audiopy',
    author='Pol Gomez Riquelme',
    author_email='polgomezriquelme@gmail.com',
    license='GPLv3',
    keywords='audio synthetizer waves manipulation',
    packages=find_packages(exclude=['contrib', 'docs', 'tests*']),
    install_requires=['matplotlib','scipy','numpy'],
    cmdclass = {'build_ext' : build_ext},
    ext_modules = [
        Extension('iotools.wav_c', ['iotools/wav_c.pyx'])
    ]
)
