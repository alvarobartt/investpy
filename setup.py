#!/usr/bin/env python

from setuptools import setup, find_packages


def readme():
    with open('README.rst') as f:
        return f.read()


setup(
    name='investing_scrapper',
    version='0.2.9',
    packages=find_packages(),
    url='',
    download_url='https://github.com/alvarob96/investing-scrapper/archive/0.2.9.tar.gz',
    license='MIT License',
    author='Álvaro Bartolomé',
    author_email='alvarob96@usal.es',
    description='This is a scrapping tool that retrieves continuous Spanish stock market information from https://es.investing.com, into a Pandas DataFrame.',
    long_description=readme(),
    install_requires=['requests', 'pandas', 'beautifulsoup4', 'pytest'],
    data_files=[
        ('tickers', ['investing_scrapper/resources/tickers.csv']),
        ('user-agents', ['investing_scrapper/resources/user-agent-list.txt'])
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
    ],
    keywords='investing, scrapper, pandas'
)
