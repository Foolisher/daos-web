# -*- coding: utf-8 -*-
import datetime
import sys
import time

__author__ = 'wanggen'

import json
import logging
import httplib2
from .base import session, app_name
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def exec_spark_job(sql, job_id, ttl):
    logging.info("rpc spark sql job:[%s]" % sql)
    conn = None
    try:
        conn = httplib2.HTTPConnectionWithTimeout('wg-mac', port=9005, timeout=60 * 10)
        conn.request(method='POST', url='/sql', body=json.dumps({"job_id": app_name+job_id, "sql": sql, "async": "true", "ttl": ttl}))
        resp = conn.getresponse()
        logging.info("SparkJob[%s] invoke response:[%s]" % (job_id, resp.read().decode()))
    except Exception as e:
        logging.error("SparkSQL job execution error:%s " % sys.exc_info()[1])
        raise e
    finally:
        conn.close()


def load_jobs():
    rows = session.execute('SELECT * FROM spark_sql_jobs')
    rows.sort(key=lambda o: o['created_at'], reverse=True)
    return rows

insert_pre = session.prepare("INSERT INTO spark_sql_jobs (app_name, job_id, hour , sql , status, ttl, created_at)"
                             " VALUES (?, ?, ?, ?, ?, ?, ?)")


def add_job(job_id, sql, hour, ttl):
    if scheduler.get_job(job_id) is not None:
        logging.warning("job[%s] has bean initiated" % job_id)
        return
    ttl = 60 * 60 * 24 * int(ttl)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session.execute(insert_pre, ['ecp', job_id, hour, sql, '1', ttl, now])
    logging.info("Add job:%s%s" % (app_name, job_id))
    scheduler.scheduled_job('cron', [sql, job_id, ttl], id=app_name+job_id, second='0', minute='0', hour=hour)(exec_spark_job)


def start_sparkjob(job_id):
    rows = session.execute("SELECT * FROM spark_sql_jobs where app_name in ('ecp','test') and job_id='%s'" % job_id)
    if len(rows) > 0:
        exec_spark_job(rows[0]['sql'], rows[0]['job_id'], rows[0]['ttl'])


def remove_job(job_id):
    try:
        session.execute("DELETE from spark_sql_jobs where  app_name = 'ecp' and job_id = '%s'" % job_id)
        session.execute("DELETE from spark_sql_job_results where  app_name = 'ecp' and job_id = '%s'" % job_id)
        scheduler.remove_job('%s%s' % (app_name, job_id))
    except Exception as e:
        logging.exception(e)


def get_result_by_jobid(job_id):
    rows = session.execute("SELECT * FROM spark_sql_job_results where app_name = 'ecp' and job_id='%s' limit 200" % job_id)
    return json.dumps(rows)


def sql_rpc(sql):
    conn = None
    try:
        sql_str = sql
        logging.info('SQL:\n[%s]\nJSON_SQL:\n[%s]', sql_str, json.dumps({"sql": sql_str}))
        conn = httplib2.HTTPConnectionWithTimeout('wg-mac', port=9005, timeout=60 * 5)
        conn.request(method='POST', url='/sql', body=json.dumps({"sql": sql_str, 'job_id': time.time()*1000000}))
        resp = conn.getresponse()
        result = resp.read().decode(encoding='UTF-8', errors='strict')
        logging.info("Query result : %s, code:%s" % (result, resp.status))
        if resp.status == 500:
            return json.dumps({"error": result})
        else:
            return '{"data": %s}' % result
    except:
        logging.exception("SparkSQL job execution error")
        return json.dumps({'error': str(sys.exc_info()[1])})
    finally:
        conn.close()


executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 300
}

scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)


# for job in session.execute('SELECT * FROM spark_sql_jobs'):
#     logging.info('Adding job: %s%s' % (app_name, job['job_id']))
#     scheduler.scheduled_job('cron', [job['sql'], job['job_id'], job['ttl']], id=app_name+job['job_id'], second='0', minute='0', hour=job['hour'])(exec_spark_job)

scheduler.start()
