#!/usr/bin/env python

# Copyright 2018-2019 Alvaro Bartolome
# See LICENSE for details.

__author__ = "Alvaro Bartolome <alvarob96@usal.es>"

import random
import pkg_resources
import os


def get_random():
    """
    This function selects a random User-Agent from the `user-agent-list` csv file, in
    order to avoid the limitations of the requests to Investing.com. The User-Agent is
    specified on the headers of the requests and is different for every request.

    ..note:
        Investing.com, via changing the User-Agent on the headers of every request, supports
        a lot of requests, since it has been tested with over 10k requests on an iteration.

    Returns:
        A :obj:`str` which is the name of a random User-Agent, which will be passed on the headers of a request.

    Raises:
        IOError: raised when `user_agent_list.csv` file was unable to retrieve or errored.
        FileNotFoundError: if `user_agent_list.csv` file has not been found.
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'user_agent_list.txt'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    if os.path.exists(file):
        with open(file, 'r') as f:
            try:
                lines = f.readlines()

                return str(random.choice(lines)).replace("\n", "")
            except IOError:
                raise IOError("ERR#0016: unable to retrieve a random user agent")
    else:
        raise FileNotFoundError("ERR#0022: user agents file not found")
