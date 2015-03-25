# coding=utf-8

from flask import Flask
import app.summary

webapp = Flask(__name__)


@webapp.route('/dealsummary')
def dealsummary():
    return app.summary.query_dealsummary()[0]


@webapp.route('/getdealsummary')
def getdealsummary():
    return app.summary.query_dealsummary()[1]


@webapp.route('/usersummary')
def usersummary():
    return app.summary.query_usersummary()[0]


if __name__ == '__main__':
    webapp.run()
