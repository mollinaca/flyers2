from setuptools import setup, find_packages
import os

here = os.path.abspath(os.path.dirname(__file__))
__version__ = "0.3"

setup(
    name="flyers2",
    version=__version__,
    description="Scripts to collect flyers from stores.",
    author="mollinaca",
    author_email="mail@mollinaca.dev",
    url="https://github.com/mollinaca/flyers2",
    python_requires=">=3.6.0",
    license="cc0",
    packages=find_packages(),
    entry_points="""
      [console_scripts]
      flyers2 = flyers2.flyers2:main
    """,
)
