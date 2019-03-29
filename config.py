# -*- coding:utf-8 -*-
# @DateTime     : 2019-03-25 13:59 
# @Author       : WangTao master
# @Email        : cs.power.supply@gmail.com
# @FileName     : config.py
# @Editor       : PyCharm

DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'master'
PASSWORD = 'djdqltj'
HOST = '192.168.204.128'
# HOST='192.168.1.150'
POST = '3306' # mariadb 的默认端口是3307 mysql 是3306
DATABASE = 'master'
DB_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST, POST, DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
