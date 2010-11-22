import os
from setuptools import setup, find_packages

data_files = []
root_dir = os.path.dirname(__file__)
if root_dir != '':
    os.chdir(root_dir)
app_dir = 'us_counties'

for dirpath, dirnames, filenames in os.walk(app_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    # Ignore any packages
    if '__init__.py' in filenames:
        pass
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])

setup(name='latimes-pluggablemaps-uscounties',
      version='alpha-0.16',
      description='L.A. Times Pluggable Maps: U.S. Counties',
      author='Ben Welsh',
      author_email='ben.welsh@gmail.com',
      url='http://github.com/datadesk/latimes-pluggablemaps-uscounties',
      download_url='http://github.com/datadesk/latimes-pluggablemaps-uscounties.git',
      packages=find_packages(),
      data_files=data_files,
      license='MIT',
      keywords='gis geographical maps earth usa counties boundaries',
      classifiers=[
       "Development Status :: 3 - Alpha",
       "Intended Audience :: Developers",
       "Intended Audience :: Science/Research",
       "License :: OSI Approved :: MIT License",
       "Operating System :: OS Independent",
       "Programming Language :: Python",
       "Topic :: Scientific/Engineering :: GIS",
       "Topic :: Software Development :: Libraries :: Python Modules"
       ],
     )
