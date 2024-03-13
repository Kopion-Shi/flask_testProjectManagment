import json

from dbutils.pooled_db import PooledDB
import pymysql.cursors
from flask import Blueprint, request

from config import config
from config import format

app_application = Blueprint("app_application", __name__, url_prefix="/api/application")

pool = PooledDB(pymysql, mincached=2, maxcached=5, host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor)  # 结果作为字典返回游标


# 返回新的书库链接对象


@app_application.route("/product", methods=["GET"])
def get_products():
    """
    :return:返回分类数据
    """
    conn = pool.connection()
    with conn.cursor() as cursor:
        sql = "SELECT `id` ,`keyCode`,`title` FROM products where `status`=0 order by `update` desc "
        cursor.execute(sql)
        data = cursor.fetchall()

    response = format.resp_format_success
    response['data'] = data
    return response


@app_application.route("/search", methods=['POST'])
def searchBykey():
    body = request.get_json()
    print(body)
    # 基础语句定义
    sql = ""

    # 获取pageSize和
    pageSize = 10 if body['pageSize'] is None else body['pageSize']
    currentPage = 1 if body['currentPage'] is None else body['currentPage']

    # 拼接查询条件
    if 'productId' in body and body['productId'] != '':
        sql = sql + " AND `productId` = '{}'".format(body['productId'])
    if 'appId' in body and body['appId'] != '':
        sql = sql + " AND `appId` LIKE '%{}%'".format(body['appId'])
    if 'note' in body and body['note'] != '':
        sql = sql + " AND `note` LIKE '%{}%'".format(body['note'])
    if 'tester' in body and body['tester'] != '':
        sql = sql + " AND `tester` LIKE '%{}%'".format(body['tester'])
    if 'developer' in body and body['developer'] != '':
        sql = sql + " AND `developer` LIKE '%{}%'".format(body['developer'])
    if 'producer' in body and body['producer'] != '':
        sql = sql + " AND `producer` LIKE '%{}%'".format(body['producer'])

    # 排序和页数拼接
    sql_data = sql + ' ORDER BY `updateDate` DESC LIMIT {},{}'.format((currentPage - 1) * pageSize, pageSize)

    # 使用连接池链接数据库
    connection = pool.connection()
    with connection:
        # 先查询总数
        with connection.cursor() as cursor:
            sql_total = 'SELECT COUNT(*) as `count` FROM apps AS A,products AS P WHERE A.productId = P.id and A.`status`=0  ' + sql
            cursor.execute(sql_total)
            total = cursor.fetchall()

        # 执行查询
        with connection.cursor() as cursor:
            # 按照条件进行查询
            sql_data = 'SELECT P.title, A.* FROM apps AS A,products AS P WHERE A.productId = P.id and A.`status`=0 ' + sql_data
            cursor.execute(sql_data)
            data = cursor.fetchall()

    # 按分页模版返回查询数据
    response = format.resp_format_success
    response['data'] = data
    response['total'] = total[0]['count']
    return response


@app_application.route("/update", methods=['POST'])
def product_update():
    # 获取传递的数据，并转换成JSON
    body = request.get_data()
    body = json.loads(body)

    # 定义默认返回体
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    # 判断必填参数
    if 'appId' not in body:
        resp_failed.message = '应用不能为空'
        return resp_failed
    elif 'tester' not in body:
        resp_failed.message = '测试负责人不能为空'
        return resp_failed
    elif 'developer' not in body:
        resp_failed.message = '测试负责人不能为空'
        return resp_failed
    elif 'producer' not in body:
        resp_failed.message = '产品负责人不能为空'
        return

    # 使用连接池链接数据库
    connection = pool.connection()

    # 判断增加或是修改逻辑
    with connection:
        # 如果传的值有ID，那么进行修改操作，否则为新增数据
        if 'id' in body and body['id'] != '':
            with connection.cursor() as cursor:
                # 拼接修改语句，由于应用名不可修改，不需要做重复校验appId
                sql = "UPDATE `apps` SET `productId`=%s, `note`=%s,`tester`=%s,`developer`=%s,`producer`=%s,`cCEmail`=%s, " \
                      "`gitCode`=%s, `wiki`=%s, `more`=%s, `creteUser`=%s, `updateUser`=%s, `updateDate`= NOW() WHERE id=%s"
                cursor.execute(sql, (
                    body["productId"], body["note"], body["tester"], body["developer"], body['producer'],
                    body["cCEmail"],
                    body["gitCode"], body["wiki"], body["more"], body["creteUser"], body["updateUser"], body["id"]))
                # 提交执行保存更新数据
                connection.commit()
        else:
            # 新增需要判断appId是否重复
            with connection.cursor() as cursor:
                select = "SELECT * FROM `apps` WHERE `appId`=%s AND `status`=0"
                cursor.execute(select, (body["appId"],))
                result = cursor.fetchall()

            # 有数据说明存在相同值，封装提示直接返回
            if len(result) > 0:
                resp_failed["code"] = 20001
                resp_failed["message"] = "唯一编码keyCode已存在"
                return resp_failed

            with connection.cursor() as cursor:
                # 拼接插入语句,并用参数化%s构造防止基本的SQL注入
                # 其中id为自增，插入数据默认数据设置的当前时间
                sql = "INSERT INTO `apps` (`appId`,`productId`,`note`,`tester`,`developer`,`producer`,`cCEmail`,`gitCode`" \
                      ",`wiki`,`more`,`creteUser`,`updateUser`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                cursor.execute(sql, (
                    body["appId"], body["productId"], body["note"], body["tester"], body["developer"], body['producer'],
                    body["cCEmail"],
                    body["gitCode"], body["wiki"], body["more"], body["creteUser"], body["updateUser"]))
                # 提交执行保存新增数据
                connection.commit()

        return resp_success
