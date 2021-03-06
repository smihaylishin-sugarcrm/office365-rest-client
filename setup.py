# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


setup(name='office365-rest-client',
      version='0.0.6',
      description='Python api wrapper for Office365 API v1.0',
      url='https://bitbucket.org/collabspot/office365-rest-client',
      author='Collabspot',
      author_email='aldwyn@collabspot.com',
      license='MIT',
      packages=find_packages(),
      install_requires=[
          'oauth2client>=4.0.0'
      ],
      zip_safe=False)
