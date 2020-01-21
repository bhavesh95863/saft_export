# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

with open('requirements.txt') as f:
	install_requires = f.read().strip().split('\n')

# get version from __version__ variable in saft_export/__init__.py
from saft_export import __version__ as version

setup(
	name='saft_export',
	version=version,
	description='SAF-T XML Export',
	author='SMB',
	author_email='jay@gmail.com',
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
