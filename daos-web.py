# -*- coding: utf-8 -*-
import datetime

import json
from json import decoder
import logging
import sys
import traceback
from flask import request
import httplib2
from flask import Flask
from app import base, summary
from app import sparkjob as sj
from app.base import app_name


logging.basicConfig(level=logging.DEBUG)
logging.getLogger('cassandra').setLevel(level=logging.WARN)

webapp = Flask(__name__)


@webapp.route('/dealsummary')
def dealsummary():
    return base.template_env.get_template("/dealsummary/view.html") \
        .render(data=summary.query_dealsummary(), component='dealsummary', js=True)


@webapp.route('/getdealsummary')
def getdealsummary():
    return json.dumps(summary.query_dealsummary())


@webapp.route('/usersummary')
def usersummary():
    return base.template_env.get_template("usersummary/view.html") \
        .render(data=summary.query_usersummary(), component='usersummary', js=True)


@webapp.route('/getusersummary')
def getusersummary():
    return json.dumps(summary.query_usersummary())


@webapp.route('/sqlshell')
def sqlshell():
    return base.template_env.get_template("sqlshell/view.html") \
        .render(component='sqlshell', js=True, css=True)


@webapp.route('/sparkjobs', methods=['GET', 'POST'])
def sparkjobs():
    return base.template_env.get_template("sparkjobs/view.html")\
        .render(data=sj.load_jobs(), component='sparkjobs', js=True, css=True)


@webapp.route('/sparkjob/add', methods=['POST'])
def add_sparkjob():
    logging.info("POST new job: %s" % request.form)
    if request.form['job_id'] != '' and request.form['sql'] != '' and request.form['hour'] != '':
        sj.add_job(request.form['job_id'], request.form['sql'], request.form['hour'], request.form['ttl'])
    return base.template_env.get_template("sparkjobs/view.html") \
        .render(data=sj.load_jobs(), component='sparkjobs', js=True, css=True)


@webapp.route('/sparkjob/jobs', methods=['GET'])
def get_jobs():
    return json.dumps(sj.load_jobs())


@webapp.route('/sparkjob/remove', methods=['PUT'])
def remove_sparkjob():
    if request.form['job_id'] != '':
        logging.info("del job job_id[%s%s]" % (app_name, request.form['job_id']))
        sj.remove_job(request.form['job_id'])
    return 'ok'


# @webapp.route('/sparkjob/start/<job_id>', methods=['GET', 'POST'])
# def start_sparkjob(job_id):
#     try:
#         sj.start_sparkjob(job_id)
#     except Exception as e:
#         logging.exception(sys.exc_info()[1])
#         return sys.exc_info()[1]
#     return 'job [%s] starting' % job_id


@webapp.route('/sparkjob/result/<job_id>')
def sparkjob_result(job_id):
    return sj.get_result_by_jobid(job_id)


@webapp.route('/sparkjob/<job_id>')
def sparkjob_view(job_id):
    return base.template_env.get_template("sparkjob/view.html") \
        .render({'job_id': job_id}, component='sparkjob', js=True, css=True)


# noinspection PyBroadException
@webapp.route('/sql', methods=['GET', 'POST'])
def sql():
    return sj.sql_rpc(request.get_data(as_text=True))


if __name__ == '__main__':
    webapp.run(debug=True)
    # webapp.run(debug=True, use_reloader=False)
