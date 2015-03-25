#!/usr/bin/env bash


kill -9 `ps -ef | grep daos-web | grep -v grep | awk '{print $2}'`