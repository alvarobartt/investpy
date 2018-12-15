#!/usr/bin/env python

import random
import pkg_resources


def get_random():
    resource_package = __name__
    resource_path = '/'.join(('resources', 'user-agent-list.txt'))
    file = pkg_resources.resource_filename(resource_package, resource_path)

    with open(file, 'r') as f:
        lines = f.readlines()
        return str(random.choice(lines)).replace("\n", "")