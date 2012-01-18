#!/usr/bin/env python
# Got from Digenpy's setup.py (http://github.com/XayOn/Digenpy)
from distutils.core import setup
import os, shutil

scripts=['FurnivallDaemon.py']

if os.name is not "posix":
    if os.name is "nt":
        import py2exe
    scripts=['FurnivallDaemon.py']

opts = {
        "py2exe": {
            'includes': '',
            "excludes": "cairo, gtk,atk,gdk",
            "dll_excludes": [
                "iconv.dll","intl.dll","libatk-1.0-0.dll",
                "libgdk_pixbuf-2.0-0.dll","libgdk-win32-2.0-0.dll",
                "libglib-2.0-0.dll","libgmodule-2.0-0.dll",
                "libgtk-win32-2.0-0.dll","libpango-1.0-0.dll",
                "libpangowin32-1.0-0.dll"],
            'packages': ['Furnivall'],
            }
        }

setup(name='Furnivall',
      version='0.1',
      download_url='https://github.com/Ibercivis/Furnivall/downloads',
      requires=['tornado', 'python_pymongo'],
      platforms=['all'],
      long_description='Furnivall collaborative science framework',
      license='GPL2+',
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
      ],
      mantainer='David Francos Cuartero (XayOn)',
      mantainer_email='xayon@xayon.net',
      description='Furnivall crowdsourcing daemon ',
      author='David Francos Cuartero (XayOn)',
      console = [{"script": "FurnivallDaemon.py" }],
      author_email='xayon@xayon.net',
      url='http://github.com/Ibercivis/Furnivall',
      packages=['Furnivall', 'Furnivall.Core', 'Furnivall.Views', 'Furnivall.Plugins'],
      scripts=scripts,
      package_data={
        'Furnivall' : [
            'static/'
            'templates/'
            ]
      },
      options=opts,
     )

