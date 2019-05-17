#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import random
import pkg_resources
import os


def get_random():
    """
    This function selects a random user agent in order to not get banned of the site due to high load of simultaneous requests.

    Returns
    -------
        :returns a string with the random user agent to use
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'user_agent_list.txt'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    try:
        if os.path.exists(file):
            with open(file, 'r') as f:
                try:
                    lines = f.readlines()

                    return str(random.choice(lines)).replace("\n", "")
                except IOError:
                    raise IOError("ERR#016: unable to retrieve a random user agent")
    except FileNotFoundError:
        raise FileNotFoundError("ERR#022: user agents file not found")
