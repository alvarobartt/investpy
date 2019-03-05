#!/usr/bin/env python

import random
import pkg_resources


def get_random():
    """
    This function selects a random user agent in order to not get banned of the site due to high load of simultaneous requests.

    Returns
    -------
        returns a string with the random user agent to use
    """

    resource_package = __name__
    resource_path = '/'.join(('resources', 'user-agent-list.txt'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    with open(file, 'r') as f:
        lines = f.readlines()
        return str(random.choice(lines)).replace("\n", "")
