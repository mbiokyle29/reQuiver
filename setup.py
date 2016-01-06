from __future__ import unicode_literals
from setuptools import setup, find_packages

setup(
    name='Requiver',
    version='0.0.1',
    packages=find_packages(exclude=['*test*']),
    install_requires=['requests', 'beautifulsoup4', 'CacheControl'],
    setup_requires=["nose>=1.3"],
    tests_require=["httmock"],
    author='Kyle McChesney',
    author_email='mbio.kyle@gmail.com',
    description='Unoffical Python Lib for querying Archer DX Quiver DB',
    license='MIT',
    keywords='Archer DX, Quiver, Gene Fusions, DB',
    url='TBD',
    classifiers=[],
    test_suite='nose.collector'
)
