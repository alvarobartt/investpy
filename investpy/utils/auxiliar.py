# Copyright 2018-2020 Alvaro Bartolome @ alvarobartt in GitHub
# See LICENSE for details.

import pandas as pd

import pkg_resources


def resource_to_data(path_to_data):
    """
    This is an auxiliar function to read data from a given resource.
    """

    resource_package = 'investpy'
    resource_path = '/'.join(('resources', path_to_data))
    if pkg_resources.resource_exists(resource_package, resource_path):
        data = pd.read_csv(pkg_resources.resource_filename(resource_package, resource_path))
    else:
        raise FileNotFoundError("ERR#0115: data file not found or errored.")

    if data is None:
        raise IOError("ERR#0115: data file not found or errored.")

    return data