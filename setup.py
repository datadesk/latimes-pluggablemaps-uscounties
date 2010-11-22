import os
from distutils.command.install import INSTALL_SCHEMES
from distutils.core import setup
import us_counties

def fullsplit(path, result=None):
    """
    Split a pathname into components (the opposite of os.path.join) in a
    platform-neutral way.
    """
    if result is None:
        result = []
    head, tail = os.path.split(path)
    if head == '':
        return [tail] + result
    if head == path:
        return result
    return fullsplit(head, [tail] + result)

# Tell distutils to put the data_files in platform-specific installation
# locations. See here for an explanation:
# http://groups.google.com/group/comp.lang.python/browse_thread/thread/35ec7b2fed36eaec/2105ee4d9e8042cb
for scheme in INSTALL_SCHEMES.values():
    scheme['data'] = scheme['purelib']

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.
packages, data_files = [], []
root_dir = os.path.dirname(__file__)
tagging_dir = os.path.join(root_dir, 'us_counties')
pieces = fullsplit(root_dir)
if pieces[-1] == '':
    len_root_dir = len(pieces) - 1
else:
    len_root_dir = len(pieces)

for dirpath, dirnames, filenames in os.walk(tagging_dir):
    # Ignore dirnames that start with '.'
    for i, dirname in enumerate(dirnames):
        if dirname.startswith('.'): del dirnames[i]
    if '__init__.py' in filenames:
        packages.append('.'.join(fullsplit(dirpath)[len_root_dir:]))
    elif filenames:
        data_files.append([dirpath, [os.path.join(dirpath, f) for f in filenames]])


setup(name='latimes-pluggablemaps-uscounties',
      version='alpha-0.17',
      description='L.A. Times Pluggable Maps: U.S. Counties',
      author='Ben Welsh',
      author_email='ben.welsh@gmail.com',
      url='http://github.com/datadesk/latimes-pluggablemaps-uscounties',
      download_url='http://github.com/datadesk/latimes-pluggablemaps-uscounties.git',
      packages=packages,
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
