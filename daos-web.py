# coding=utf-8

from flask import Flask
import app.summary as summary


app = Flask(__name__)


@app.route('/dealsummary')
def dealsummary():
    return summary.query_dealsummary()

@app.route('/usersummary')
def usersummary():
    return summary.query_usersummary()


if __name__ == '__main__':
    app.run()
