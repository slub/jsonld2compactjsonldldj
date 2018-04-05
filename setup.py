"""
A commandline command (Python3 program) that transforms a given JSON-LD record array to line-delimited, compact JSON-LD records
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='jsonld2compactjsonldldj',
      version='0.0.1',
      description='a commandline command (Python3 program) that transforms a given JSON-LD record array to line-delimited, compact JSON-LD records',
      url='https://github.com/slub/jsonld2compactjsonldldj',
      author='Bo Ferri',
      author_email='zazi@smiy.org',
      license="Apache 2.0",
      packages=[
          'jsonld2compactjsonldldj',
      ],
      package_dir={'jsonld2compactjsonldldj': 'jsonld2compactjsonldldj'},
      install_requires=[
          'argparse>=1.4.0',
          'pyld>=1.0.3'
      ],
      entry_points={
          "console_scripts": ["jsonld2compactjsonldldj=jsonld2compactjsonldldj.jsonld2compactjsonldldj:run"]
      }
      )
