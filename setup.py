from setuptools import setup

setup(
    name='investing_scrapper',
    version='0.1',
    packages=['', 'investing_scrapper'],
    url='',
    license='MIT License',
    author='Álvaro Bartolomé',
    author_email='alvarob96@usal.es',
    description='This is a scrapping tool that retrieves continuous Spanish stock market information from https://es.investing.com, into a Pandas DataFrame.',
    install_requires=['requests', 'pandas', 'beautifulsoup4', 'unidecode']
)
