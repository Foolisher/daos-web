#!/usr/bin/env bash

# wget https://bootstrap.pypa.io/ez_setup.py -O - | python - --user
# wget https://pypi.python.org/packages/source/p/pip/pip-6.0.8.tar.gz && tar xvf pip-6.0.8.tar.gz && cd pip-6.0.8 && python setup.py install

# pip install flask; pip install jinja2; pip install cassandra-driver;

ssh wanggen@wg-linux mkdir -p /home/wanggen/projects/daos/
scp -r . wg-linux:/home/wanggen/projects/daos/
ssh admin@10.0.0.8 mkdir -p /home/admin/projects/daos-web/
scp -r . admin@10.0.0.8:/home/admin/projects/daos-web/