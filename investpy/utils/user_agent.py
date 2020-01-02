#!/usr/bin/python3

# Copyright 2018-2020 Alvaro Bartolome @ alvarob96 in GitHub
# See LICENSE for details.

import random
import pkg_resources
import os


def get_random():
    """
    This function selects a random User-Agent from the `user-agent-list` csv file, in
    order to avoid the limitations of the requests to Investing.com. The User-Agent is
    specified on the headers of the requests and is different for every request.

    Note that Investing.com, via changing the User-Agent on the headers of every request, allows
    a lot of requests, since it has been tested with over 10k consecutive requests without getting
    any HTTP error code from Investing.com.

    Returns:
        :obj:`str` - user_agent:
            The returned :obj:`str` is the name of a random User-Agent, which will be passed on the 
            headers of a request so to avoid restrictions due to the use of multiple requests from the 
            same User-Agent.

    Raises:
        IOError: raised when `user_agent_list.csv` file was unable to retrieve or errored.
        FileNotFoundError: raised if `user_agent_list.csv` file has not been found.
    
    """

    resource_path = '/'.join(('resources', 'user_agent_list.txt'))
    file_ = pkg_resources.resource_filename('investpy', resource_path)

    if os.path.exists(file_):
        with open(file_, 'r') as f:
            content = f.read(1)

            if content:
                lines = f.readlines()

                return str(random.choice(lines)).replace("\n", "")
            else:
                raise IOError("ERR#0016: unable to retrieve a random user agent")
    else:
        raise FileNotFoundError("ERR#0022: user agents file not found")


def clear_file():
    """
    This function clears out the content of `user_agent_list.txt` file so to improve code coverage as to test 
    the whole functionality of `investpy.utils.user_agent.get_random()` function. When the content of the file 
    is cleared out, the next time that the function `investpy.utils.user_agent.get_random()` is called, it is going 
    to raise an `IOError` due to missing content on file `user_agent_list.txt`.
    """

    resource_path = '/'.join(('resources', 'user_agent_list.txt'))
    file_ = pkg_resources.resource_filename('investpy', resource_path)

    if os.path.exists(file_):
        with open(file_, 'w') as f:
            f.close()


def delete_file():
    """
    This function deletes `user_agent_list.txt` file so to improve code coverage as to test the whole functionality 
    of `investpy.utils.user_agent.get_random()` function. When file is missing, the next time that the function 
    `investpy.utils.user_agent.get_random()` is called, it is going to raise a `FileNotFoundError` due to missing file 
    `user_agent_list.txt`.
    """

    resource_path = '/'.join(('resources', 'user_agent_list.txt'))
    file_ = pkg_resources.resource_filename('investpy', resource_path)

    if os.path.exists(file_):
        os.remove(file_)
