# -*- coding: utf-8 -*-

"""
    base environment container for
        jinja2 template environment
        and cassandra environment(session)
"""

import logging
from cassandra.cluster import Cluster
from cassandra.decoder import dict_factory

from jinja2 import Environment, PackageLoader


logging.basicConfig(level=logging.DEBUG)

__author__ = 'wanggen'

template_env = Environment(loader=PackageLoader(package_name='components', package_path='/'))
session = Cluster(contact_points=["wg-linux"]).connect("terminus_data")
session.row_factory = dict_factory

app_name='ecp-'
