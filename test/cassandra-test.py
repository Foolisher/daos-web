from _codecs import decode, encode
import datetime
from uuid import UUID, uuid4, uuid5, uuid1
import uuid
from cassandra.cluster import Cluster

import toolz.utils as utils
import toolz.dicttoolz as dicttoolz
import toolz.functoolz as functoolz

functoolz

__author__ = 'wanggen'


session = Cluster(contact_points=["wg-linux"]).connect("groupon")

session.execute("""
 create table if not exists test(id text primary key, values list<text>)
""")

limit = 100

insert_pre = session.prepare('insert into test(id, values) values(?, ?)')
update_pre = session.prepare('update test set values=values+? where id=?')

start = datetime.datetime.now().timestamp()

print(session.execute("SELECT * FROM test where id='1'"))

for n in range(1,1):
    print(session.execute("SELECT * FROM test where id='1'")[0])
# for n in range(1, limit):
#     ids = []
#     for len in range(1,1000):
#         ids.append(str(uuid1()))
#     # session.execute(insert_pre, parameters=[str(n), [str(uuid1())]])
#     session.execute(update_pre, parameters=[ids, str(n)])
print("exec %s 条数据耗时: %s second" % (limit, (datetime.datetime.now().timestamp()-start))) #





# for row in session.execute("select * from spark_sql_job_results"):
#     print(row)