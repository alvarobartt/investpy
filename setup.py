# Copyright 2018-2020 Alvaro Bartolome @ alvarobartt in GitHub
# See LICENSE for details.

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()

def requirements():
    reqs = list()
    with io.open('requirements.txt', encoding='utf-8') as f:
        for line in f.readlines():
            reqs.append(line.strip())
    return reqs


setup(
    name='investpy',
    version='1.0',
    packages=find_packages(),
    url='https://investpy.readthedocs.io/',
    download_url='https://github.com/alvarobartt/investpy/archive/1.0.tar.gz',
    license='MIT License',
    author='Alvaro Bartolome',
    author_email='alvarobartt@usal.es',
    description='investpy — a Python package for financial data extraction from Investing',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=requirements(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
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
        'Bug Reports': 'https://github.com/alvarobartt/investpy/issues',
        'Source': 'https://github.com/alvarobartt/investpy',
        'Documentation': 'https://investpy.readthedocs.io/'
    },
)
