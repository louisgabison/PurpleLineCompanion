import requests
import jsons

import uuid
import pathlib
import logging
import sys
import os
import base64
import time
import datatier

from configparser import ConfigParser
from getpass import getpass

dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)

def check_arrival_time(baseurl):
    try:
        print("Please input a station ID")
        station_id = input()
        api = '/train-times'
        url = baseurl+api+"?station_id="+ station_id
        res = requests.get(url)
        if res.status_code != 200:
            body = res.json()
            print("**ERROR:", body)
            return
        else:
            body = res.json()
            #CHECK
            print(body)
        

    except Exception as e:
        print("**ERROR**")
        logging.error("check_arrival_time() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return None

def sns(baseurl):
    try:
        email = input("Please input your email address")
        station_id = input("Please input your station_id")
        sql = """INSERT INTO subscriptions (email, station_id) VALUES (%s,%s)"""
        response = datatier.perform_action(dbConn, sql, (email, station_id))
        print(f"Subscription added: {email} for station {station_id}")

    except Exception as e:
        print("**ERROR**")
        logging.error("sns() failed:")
        logging.error("url: " + url)
        logging.error(e)
        return None


try:
    while True:
        print("Welcome to the Purple Line Companion app!")
        print(">> Enter a command:")
        print("0 => Quit")
        print("1 => Check arrival times")
        print("2 => Schedule notification service")
        print("3 => Suggest a song")
        cmd = input()
        if cmd == 0:
            break
        elif cmd == 1:
            check_arrival_time(baseurl)
        elif cmd == 2:
            sns(baseurl)
        elif cmd == 3:
            suggest_song(baseurl)
        else:
            print("Invalid option")
            pass



except Exception as e:
  logging.error("**ERROR: main() failed:")
  logging.error(e)
  sys.exit(0)