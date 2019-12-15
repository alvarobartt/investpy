#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


def parse_requirements():
    requirements = list()
    with io.open('requirements.txt', encoding='utf-8') as f:
        for line in f.readlines():
            requirements.append(line.strip())
    return requirements


setup(
    name='investpy',
    version='0.9.11',
    packages=find_packages(),
    url='https://investpy.readthedocs.io/',
    download_url='https://github.com/alvarob96/investpy/archive/0.9.11.tar.gz',
    license='MIT License',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='investpy — a Python package for financial historical data extraction from Investing',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=parse_requirements(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries"
    ],
    keywords=', '.join([
        'investing', 'investing-api', 'historical-data',
        'financial-data', 'stocks', 'funds', 'etfs',
        'indices', 'currency crosses', 'bonds', 'commodities',
        'crypto currencies'
    ]),
    python_requires='>=3',
    project_urls={
        'Bug Reports': 'https://github.com/alvarob96/investpy/issues',
        'Source': 'https://github.com/alvarob96/investpy',
        'Documentation': 'https://investpy.readthedocs.io/'
    },
)
