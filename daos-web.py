# coding=utf-8

from flask import Flask, json
from jinja2 import Environment, PackageLoader
from cassandra.cluster import Cluster
import logging

app = Flask(__name__)

env = Environment(loader=PackageLoader('daos-web', '.'))

cluster = Cluster(contact_points=["wg-linux"])
session = cluster.connect("groupon")

@app.route('/')
def index():
    return env.get_template("components/index.html").render()


@app.route('/dealsummary')
def summary():
    try:
        page = env.get_template("components/dealsummary/view.html")\
            .render(data=do_query(), component='dealsummary')
    except:
        logging.exception("error")
        raise
    return page
    # return json.jsonify({'data': do_query()})


def do_query():
    try:
        data_list = []
        rows = session.execute("SELECT * from groupon_summary_deals")
        for row in rows:
            record = {
                'sum_for':      row.sum_for.strftime('%Y-%m-%d'),
                'deal':         row.deal/100,
                'deal_item':    row.deal_item,
                'deal_order':   row.deal_order,
                'gmv':          row.gmv,
                'gross_item':   row.gross_item,
                'gross_order':  row.gross_order,
                'per_order':    row.per_order
            }
            data_list.append(record)
        data_list.sort(key=lambda r: r['sum_for'], reverse=True)
        return data_list
    except:
        logging.error("未知异常")
        raise

if __name__ == '__main__':
    app.run()
