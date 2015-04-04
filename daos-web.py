# -*- coding: utf-8 -*-
import datetime

import json
from json import decoder
import logging
import sys
import traceback
from flask.helpers import url_for

logging.basicConfig(level=logging.DEBUG)
logging.getLogger('cassandra').setLevel(level=logging.WARN)
from flask import request, redirect
import httplib2
from flask import Flask
from app import base, summary
from app import sparkjob as sj

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


@webapp.route('/sparkjob', methods=['GET', 'POST'])
def sparkjob():
    if request.method == 'POST':
        logging.info("POST new job: %s" % request.form)
        if request.form['job_id'] != '' and request.form['sql'] != '' and request.form['hour'] != '':
            sj.add_job(request.form['job_id'], request.form['sql'], request.form['hour'], request.form['ttl'])
    return base.template_env.get_template("sparkjob/view.html")\
        .render(data=sj.load_jobs(), component='sparkjob', js=True, css=True)


@webapp.route('/sparkjob/remove', methods=['PUT'])
def remove_sparkjob():
    if request.form['job_id'] != '':
        logging.info("del job job_id[%s]" % request.form['job_id'])
        sj.remove_job(request.form['job_id'])
    return 'ok'


@webapp.route('/sparkjob/result/<job_id>')
def get_sparkjob_result(job_id):
    return sj.get_result_by_jobid(job_id)


# noinspection PyBroadException
@webapp.route('/sql', methods=['GET', 'POST'])
def sql():
    conn = None
    try:
        sql_str = request.get_data(as_text=True)
        logging.info('SQL:\n[%s]\nJSON_SQL:\n[%s]', sql_str, json.dumps({"sql": sql_str}))
        conn = httplib2.HTTPConnectionWithTimeout('wg-mac', port=9005, timeout=60 * 5)
        conn.request(method='POST', url='/sql', body=json.dumps({"sql": sql_str}))
        resp = conn.getresponse()
        result = resp.read().decode(encoding='UTF-8', errors='strict')
        logging.info("Query result : %s, code:%s" % (result, resp.code))
        if resp.code == 500:
            return json.dumps({"error": result})
        else:
            return '{"data": %s}' % result
    except:
        logging.exception("SparkSQL job execution error")
        return json.dumps({'error': str(sys.exc_info()[1])})
    finally:
        conn.close()


if __name__ == '__main__':
    webapp.run(debug=True)
    # webapp.run(debug=True, use_reloader=False)
