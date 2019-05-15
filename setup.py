#!/usr/bin/env python

from setuptools import setup, find_packages
import io


def readme():
    with io.open('README.md', encoding='utf-8') as f:
        return f.read()


setup(
    name='investpy',
    version='0.8.4.4',
    packages=find_packages(),
    url='https://github.com/alvarob96/investpy',
    download_url='https://github.com/alvarob96/investpy/archive/0.8.4.4.tar.gz',
    license='MIT License',
    author='Alvaro Bartolome',
    author_email='alvarob96@usal.es',
    description='investpy — a Python package for historical data extraction from the spanish stock market',
    long_description=readme(),
    long_description_content_type='text/markdown',
    install_requires=['requests==2.21.0', 'pandas==0.24.2', 'unidecode==1.0.23', 'lxml==4.3.3', 'pytest==4.1.1'],
    data_files=[
        ('equities_es', ['investpy/resources/es/equities.csv']),
        ('funds_es', ['investpy/resources/es/funds.csv']),
        ('etfs_es', ['investpy/resources/es/etfs.csv']),
        ('user_agents', ['investpy/resources/user_agent_list.txt'])
    ],
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
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
    keywords='investing-api, spanish-stock-market, scraper, historical-data, financial-data, stock'
)
