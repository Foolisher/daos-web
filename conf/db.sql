

drop table spark_sql_jobs;
CREATE TABLE spark_sql_jobs(
  job_id          text PRIMARY KEY,
  last_time_cost  int,
  last_exec_stat  int,
  sql             text,
  hour            text,
  ttl             int,
  status          text,
  created_at      text
) with comment='SparkSQL job definitions'
;



drop table spark_sql_job_results;
CREATE TABLE spark_sql_job_results(
  job_id      text,
  datetime    text,
  rowid       int,
  result      text,
  PRIMARY KEY(job_id, datetime, rowid)
)with clustering order by(datetime DESC, rowid ASC )
;

