

CREATE KEYSPACE groupon WITH REPLICATION = { 'class' : 'NetworkTopologyStrategy', 'datacenter1' : 2 };

drop table spark_sql_jobs;
CREATE TABLE spark_sql_jobs(
  job_id          text PRIMARY KEY,
  last_time_cost  int,
  last_exec_stat  int,
  sql             text,
  day             text,
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
  result      text,
  rowid       text,
  PRIMARY KEY(job_id, datetime, rowid)
)with clustering order by(datetime DESC)
;



select substr(created_at, 0, 10) date,
       count(distinct(IF(status==0 or status==-6 or status==-7, 0, order_id)))-1 paid_orders,
       sum(IF(status==0 or status==-6 or status==-7, 0, quantity)) paid_items,
       count(distinct(order_id)) ordered_orders,
       sum(quantity) ordered_items,
       sum(IF(status==0 or status==-6 or status==-7, 0, fee))/100 paid_amount,
       sum(fee)/100 ordered_amount
from ecp_order_items
group by substr(created_at, 0, 10)
order by date desc