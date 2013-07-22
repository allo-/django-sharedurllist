from setuptools import setup
import os

try:
    reqs = open(os.path.join(os.path.dirname(__file__),
                'requirements.txt')).read()
except (IOError, OSError):
    reqs = ''

setup(name='sharedurllist',
      version="1.0",
      description='Django App for sharing URLs between different devices',
      long_description='Django App for sharing URLs between different devices',
      author='Alexander Schier',
      author_email='allo@laxu.de',
      url='',
      packages=['sharedurllist'],
      include_package_data=True,
      install_requires=reqs,
      classifiers=[
          'Framework :: Django',
          ],
      )
