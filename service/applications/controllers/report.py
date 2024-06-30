from flask import Blueprint
from dbutils.pooled_db import PooledDB
from service.config import config, format

from flask import request
import pymysql.cursors

# 使用数据库连接池的方式链接数据库，提高资源利用率
pool = PooledDB(pymysql, mincached=4, maxcached=10, host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor, blocking=True)
connection = pool.connection()
test_report = Blueprint("test_report", __name__)

@test_report.route("/api/report/info", methods=['GET'])
def getTestReoprt():
    report_id = request.args.get('id')
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    if not report_id:
        resp_failed.message = '提测 id 不能为空'
        return resp_failed
    connection = pool.connection()
    with connection.cursor() as cursor:
        # 查询提测信息表，返回报告所需要的字段值
        sql = "SELECT id,status,test_desc,test_risks,test_cases,test_bugs,test_file,test_note,test_email FROM request WHERE id={}".format(
            report_id)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 1:
            resp_success['data'] = data[0]
    return resp_success
