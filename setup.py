#!/usr/bin/env python

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='investpy',
    version='0.3.6',
    packages=find_packages(),
    url='',
    download_url='https://github.com/alvarob96/investpy/archive/0.3.9.tar.gz',
    license='MIT License',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='This is a scraping tool that retrieves continuous Spanish stock market information from Investing.com, into a Pandas DataFrame.',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=['requests==2.21.0', 'pandas==0.23.4', 'beautifulsoup4==4.7.1', 'pytest==4.1.1'],
    data_files=[
        ('equities', ['investpy/resources/equities.csv']),
        ('funds', ['investpy/resources/funds.csv']),
        ('user-agents', ['investpy/resources/user-agent-list.txt'])
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
    keywords='investing, investment, scraper, pandas, finance, stock, funds, etf, api'
)
