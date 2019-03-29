# -*- coding:utf-8 -*-
# @DateTime     : 2019-03-26 15:41 
# @Author       : WangTao master
# @Email        : cs.power.supply@gmail.com
# @FileName     : mySQL.py
# @Editor       : PyCharm
import sqlite3

import pymysql
from flask import Flask, redirect, render_template

app = Flask(__name__)


# 创建MySql连接,执行SQL查询语句,把连接返回.

def db_connect(sql):
    # pymysql.Connect()参数说明
    # host(str):      MySQL服务器地址
    # port(int):      MySQL服务器端口号
    # user(str):      用户名
    # passwd(str):    密码
    # db(str):        数据库名称
    # charset(str):   连接编码
    #
    # connection对象支持的方法
    # cursor()        使用该连接创建并返回游标
    # commit()        提交当前事务
    # rollback()      回滚当前事务
    # close()         关闭连接
    #
    # cursor对象支持的方法
    # execute(op)     执行一个数据库的查询命令
    # fetchone()      取得结果集的下一行
    # fetchmany(size) 获取结果集的下几行
    # fetchall()      获取结果集中的所有行
    # rowcount()      返回数据条数或影响行数
    # close()         关闭游标对象

    # MySQLdb默认查询结果都是返回tuple，通过使用不同的游标可以改变输出格式，这里传递一个cursors.DictCursor参数。

    db = pymysql.connect(host="192.168.204.128",
                         port=3306,
                         user="master",
                         passwd="djdqltj",
                         db="master",
                         charset='utf8mb4',
                         cursorclass=pymysql.cursors.DictCursor)
    cursor = db.cursor()
    cursor.execute(sql)
    results = cursor.fetchall()
    db.close()
    return results


def dict_factory(cursor, row):  # sqlite 查询返回字典类型 这是官方文档的说法
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def sqlite_conn():
    conn = sqlite3.connect('master.db')  # 连接数据库
    conn.row_factory = dict_factory # 定义查询返回类型 ，这里表示为返回字典
    db = conn.cursor()  # 定义游标

    # db.execute('insert into user (id, name) values (\'2\', \'Michael\')')
    # print('-------------',str(db.rowcount))

    # conn.commit() 提交修改事务
    rs = db.execute('select * from user').fetchall()  # 执行SQL
    # 关闭游标，关闭连接
    db.close()
    conn.close()
    return rs


@app.route('/mysql-demo')
def index():
    sql = 'select * from atricle'  # where 1=2'
    rs = db_connect(sql)
    print(type(rs))
    print(len(rs))
    # 判断查询到的数据是否为空
    if rs:
        return render_template('mysql-test01.html', book=rs)
    else:
        return '没有查询到数据'


@app.route('/sqlite-demo')
def sqlite_demo():
    rs = sqlite_conn()
    print(rs)
    print('sqlite OK')
    if rs:
        return render_template('sqlite-test01.html', book=rs)
    else:
        return '没有查询到数据'


if __name__ == '__main__':
    app.run(debug=True)
