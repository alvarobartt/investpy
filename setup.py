from setuptools import setup, find_packages

setup(
    name='investing_scrapper',
    version='0.2.6',
    packages=find_packages(),
    url='',
    download_url='https://github.com/alvarob96/investing-scrapper/archive/0.2.6.tar.gz',
    license='MIT License',
    author='Álvaro Bartolomé',
    author_email='alvarob96@usal.es',
    description='This is a scrapping tool that retrieves continuous Spanish stock market information from https://es.investing.com, into a Pandas DataFrame.',
    install_requires=['requests', 'pandas', 'beautifulsoup4'],
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
