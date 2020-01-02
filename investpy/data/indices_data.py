#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import json

import pandas as pd
import pkg_resources

import unidecode


def indices_as_df(country=None):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`pandas.DataFrame` with all the information of every available index. If the country
    filtering is applied, just the indices from the introduced country are going to be returned.
    All the available indices can be found at: https://www.investing.com/indices/world-indices and at
    https://www.investing.com/indices/world-indices, since both world and global indices are retrieved.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.

    Returns:
        :obj:`pandas.DataFrame` - indices_df:
            The resulting :obj:`pandas.DataFrame` contains all the indices information retrieved from Investing.com,
            as previously listed by investpy.

            In case the information was successfully retrieved, the :obj:`pandas.DataFrame` will look like::

                country | name | full_name | symbol | currency | class | market
                --------|------|-----------|--------|----------|-------|--------
                xxxxxxx | xxxx | xxxxxxxxx | xxxxxx | xxxxxxxx | xxxxx | xxxxxx

    Raises:
        ValueError: raised if any of the introduced parameters is missing or errored.
        FileNotFoundError: raised if the `indices.csv` file was not found.
        IOError: raised if the `indices.csv` file from `investpy` is missing or errored.
    
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0059: indices file not found or errored.")

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    indices.drop(columns=['tag', 'id'], inplace=True)

    if country is None:
        indices.reset_index(drop=True, inplace=True)
        return indices
    elif unidecode.unidecode(country.lower()) in index_countries_as_list():
        indices = indices[indices['country'] == unidecode.unidecode(country.lower())]
        indices.reset_index(drop=True, inplace=True)
        return indices


def indices_as_list(country=None):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`list` with the names of every available index. If the country filtering is applied, just
    the indices from the introduced country are going to be returned.
    All the available indices can be found at: https://www.investing.com/indices/world-indices and at
    https://www.investing.com/indices/world-indices, since both world and global indices are retrieved.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.

    Returns:
        :obj:`list` - indices_list:
            The resulting :obj:`list` contains the retrieved data, which corresponds to the index names of
            every index listed in Investing.com.

            In case the information was successfully retrieved, the :obj:`list` will look like::

                indices = ['S&P Merval', 'S&P Merval Argentina', 'S&P/BYMA Argentina General', ...]

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if the `indices.csv` file was not found.
        IOError: raised if the `indices.csv` file is missing or errored.
    
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0059: indices file not found or errored.")

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    indices.drop(columns=['tag', 'id'], inplace=True)

    if country is None:
        return indices['name'].tolist()
    elif unidecode.unidecode(country.lower()) in index_countries_as_list():
        return indices[indices['country'] == unidecode.unidecode(country.lower())]['name'].tolist()


def indices_as_dict(country=None, columns=None, as_json=False):
    """
    This function retrieves all the available `indices` from Investing.com as previously listed in investpy, and
    returns them as a :obj:`dict` with all the information of every available index. If the country
    filtering is applied, just the indices from the introduced country are going to be returned. Additionally, the
    columns to retrieve data from can be specified as a parameter formatted as a :obj:`list`.
    All the available indices can be found at: https://www.investing.com/indices/world-indices and at
    https://www.investing.com/indices/world-indices, since both world and global indices are retrieved.

    Args:
        country (:obj:`str`, optional): name of the country to retrieve all its available indices from.
        columns (:obj:`list` of :obj:`str`, optional): description
            a :obj:`list` containing the column names from which the data is going to be retrieved.
        as_json (:obj:`bool`, optional): description
            value to determine the format of the output data (:obj:`dict` or :obj:`json`).

    Returns:
        :obj:`dict` or :obj:`json` - indices_dict:
            The resulting :obj:`dict` contains the retrieved data if found, if not, the corresponding
            fields are filled with `None` values.

            In case the information was successfully retrieved, the :obj:`dict` will look like::

                indices_dict = {
                    'country': country,
                    'name': name,
                    'full_name': full_name,
                    'symbol': symbol,
                    'currency': currency,
                    'class': class,
                    'market': market
                }

    Raises:
        ValueError: raised whenever any of the introduced arguments is not valid or errored.
        FileNotFoundError: raised if the `indices.csv` file was not found.
        IOError: raised if the `indices.csv` file is missing or errored.
    
    """

    if country is not None and not isinstance(country, str):
        raise ValueError("ERR#0025: specified country value not valid.")

    if not isinstance(as_json, bool):
        raise ValueError("ERR#0002: as_json argument can just be True or False, bool type.")

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0059: indices file not found or errored.")

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")

    indices.drop(columns=['tag', 'id'], inplace=True)

    if columns is None:
        columns = indices.columns.tolist()
    else:
        if not isinstance(columns, list):
            raise ValueError("ERR#0020: specified columns argument is not a list, it can just be list type.")

    if not all(column in indices.columns.tolist() for column in columns):
        raise ValueError("ERR#0023: specified columns does not exist, available columns are "
                         "<country, name, full_name, symbol, currency, class, market>")

    if country is None:
        if as_json:
            return json.dumps(indices[columns].to_dict(orient='records'))
        else:
            return indices[columns].to_dict(orient='records')
    elif country in index_countries_as_list():
        if as_json:
            return json.dumps(indices[indices['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records'))
        else:
            return indices[indices['country'] == unidecode.unidecode(country.lower())][columns].to_dict(orient='records')


def index_countries_as_list():
    """
    This function retrieves all the country names indexed in Investing.com with available indices to retrieve data
    from, via reading the `indices.csv` file from the resources directory. So on, this function will display a listing
    containing a set of countries, in order to let the user know which countries are available for indices data retrieval.

    Returns:
        :obj:`list` - countries:
            The resulting :obj:`list` contains all the available countries with indices as indexed in Investing.com

    Raises:
        FileNotFoundError: raised if the `indices.csv` file was not found.
        IOError: raised if the `indices.csv` file is missing or errored.
    
    """

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', 'indices', 'indices.csv'))
    if pkg_resources.resource_exists(resource_package, resource_path):
        indices = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0059: indices file not found or errored.")

    if indices is None:
        raise IOError("ERR#0037: indices not found or unable to retrieve.")
    else:
        return indices['country'].unique().tolist()
