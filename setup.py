#!/usr/bin/env python

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='investing_scrapper',
    version='0.3.5',
    packages=find_packages(),
    url='',
    download_url='https://github.com/alvarob96/investing-scrapper/archive/0.3.5.tar.gz',
    license='MIT License',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='This is a scrapping tool that retrieves continuous Spanish stock market information from investing, into a Pandas DataFrame.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=['requests==2.21.0', 'pandas==0.23.4', 'beautifulsoup4==4.7.1', 'pytest==4.1.1'],
    data_files=[
        ('equities', ['investing_scrapper/resources/equities.csv']),
        ('funds', ['investing_scrapper/resources/funds.csv']),
        ('user-agents', ['investing_scrapper/resources/user-agent-list.txt'])
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Investment",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator",
        "Topic :: Software Development :: Libraries",
        "Operating System :: OS Independent",
    ],
    keywords='investing, scrapper, pandas, finance, stock, api'
)
