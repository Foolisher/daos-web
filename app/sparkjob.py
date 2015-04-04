# -*- coding: utf-8 -*-
import datetime

__author__ = 'wanggen'

import json
import logging
import httplib2
from .base import session
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


def exec_spark_job(sql, job_id, ttl):
    logging.info("rpc spark sql job:[%s]" % sql)
    conn = None
    try:
        conn = httplib2.HTTPConnectionWithTimeout('wg-mac', port=9005, timeout=60 * 10)
        conn.request(method='POST', url='/sql', body=json.dumps({"job_id": job_id, "sql": sql, "async": "true", "ttl": ttl}))
        resp = conn.getresponse()
        logging.info("SparkJob[%s] invoke response:[%s]" % (job_id, resp.read().decode()))
    except Exception:
        logging.error("SparkSQL job execution error")
    finally:
        conn.close()


def load_jobs():
    rows = session.execute('SELECT * FROM spark_sql_jobs')
    rows.sort(key=lambda o: o.created_at, reverse=True)
    return rows


def add_job(job_id, sql, hour, ttl):
    if scheduler.get_job(job_id) is not None:
        logging.warning("job[%s] has bean initiated" % job_id)
        return
    ttl = 60 * 60 * 24 * int(ttl)
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    session.execute \
        ("INSERT INTO spark_sql_jobs (job_id, hour , sql , status, ttl, created_at) VALUES ('%s', '%s', '%s', '%s', %s, '%s')" % (
            job_id, hour, sql, '1', ttl, now))
    logging.info("Add job:%s" % job_id)
    scheduler.scheduled_job('cron', [sql, job_id, ttl], id=job_id, second='0', minute='0', hour=hour)(exec_spark_job)


def remove_job(job_id):
    scheduler.remove_job(job_id)
    session.execute("DELETE from spark_sql_jobs where job_id = '%s'" % job_id)


def get_result_by_jobid(job_id):
    rows = session.execute("SELECT * FROM spark_sql_job_results where job_id='%s'" % job_id)
    data_list = []
    for row in rows:
        record = {
            'job_id':     row.job_id,
            'datetime':   row.datetime,
            'rowid':      row.rowid,
            'result':     row.result
        }
        data_list.append(record)
    return json.dumps(data_list)


executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 30
}

scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)


for job in session.execute('SELECT * FROM spark_sql_jobs'):
    job_scheduler = scheduler.get_job(job.job_id)
    if job_scheduler is not None:
        logging.warning("job[%s] has bean initiated" % job.job_id)
        continue
    logging.info("Add spark job[%s] hour[%s] sql[%s]" % (job.job_id, job.hour, job.sql[0:20]))
    scheduler.scheduled_job('cron', [job.sql, job.job_id, job.ttl], id=job.job_id, second='0', minute='0', hour=job.hour)(exec_spark_job)

scheduler.start()
