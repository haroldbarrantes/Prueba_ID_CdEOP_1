""" Setup file """
from setuptools import setup
import versioneer


setup(    
    name = 'vedd-prueba-cdeop',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
)
