
from setuptools import setup,find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from subprocess import check_call
from glob import glob
import os
import sys
current_path  = os.path.dirname(os.path.realpath(__file__))

setup(
    name='wgetter',
    version='1.0',
    # cmdclass={'develop': PostDevelopCommand,'install': PostInstallCommand},
    packages=['wgetter'],
    entry_points ={'console_scripts': ['wgetter = wgetter.wgetter:threaded_wget']}
)
