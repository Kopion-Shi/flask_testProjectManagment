# -*- coding:utf-8 -*-
from multiprocessing import connection

import pymysql.cursors
from flask import Blueprint, request

app_product = Blueprint("app_product", __name__)


def connectDB():
    connection = pymysql.connect(host='localhost',  # 数据库IP地址或链接域名
                                 user='root',  # 设置的具有增改查权限的用户
                                 password='root',  # 用户对应的密码
                                 database='tpmstore',  # 数据表
                                 charset='utf8mb4',  # 字符编码
                                 cursorclass=pymysql.cursors.DictCursor)  # 结果作为字典返回游标
    # 返回新的书库链接对象
    return connection


@app_product.route("/api/product/list", methods=["GET"])
def product_list():
    connection = connectDB()
    # 硬编码返回list
    with connection.cursor() as cursor:
        sql = "select * from Products where status=0 ORDER BY 'UPDATE' DESC;"
        cursor.execute(sql)
        data = cursor.fetchall()
    # 按返回模版格式进行json结果返回
    resp_data = {"code": 20000, "data": data}

    return resp_data


@app_product.route("/api/product/create", methods=["POST"])
def product_create():
    body = request.get_json()
    connection = connectDB()
    resp_data = {"code": 20000, "message": "success", "data": {}}
    with connection.cursor() as cursor:
        select = f"select * from Products where keyCode='{body['keyCode']}'AND status=0"
        cursor.execute(select, )
        data = cursor.fetchall()

    if len(data) > 0:
        resp_data["code"] = 20001
        resp_data["message"] = "唯一编码keyCode存在"
        return resp_data
    with connection.cursor() as cursor:
        sql = "INSERT INTO `products` (`keyCode`,`title`,`desc`,`operator`) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (body["keyCode"], body["title"], body["desc"], body["operator"]))
        connection.commit()

    return resp_data


@app_product.route("/api/product/update", methods=["POST"])
def product_update():
    body = request.get_json()
    connection = connectDB()
    resp_data = {"code": 20000, "message": "success", "data": {}}
    with connection.cursor() as cursor:
        select = f"select * from Products where keyCode='{body['keyCode']}' AND status=0;"
        cursor.execute(select, )
        data = cursor.fetchall()

    if len(data) > 0 and data[0]["id"] != body["id"]:
        resp_data["code"] = 20001
        resp_data["message"] = "唯一编码keyCode存在"
        return resp_data

    with connection.cursor() as cursor:
        sql = "update `products` set `keyCode`=%s, `title`=%s,`desc`=%s,`operator`= %s where id=%s;"
        cursor.execute(sql, (body["keyCode"], body["title"], body["desc"], body["operator"], body["id"]))
        connection.commit()

    return resp_data


# [DELETE方法]根据id实际删除项目信息
@app_product.route("/api/product/delete", methods=['DELETE'])
def product_delete():
    # 返回的reponse
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }
    # 方式1：通过params 获取id
    ID = request.args.get('id')
    # 做个参数必填校验
    if ID is None:
        resp_data["code"] = 20002
        resp_data["message"] = "请求id参数为空"
        return resp_data
    # 重新链接数据库
    connection = connectDB()
    with connection.cursor() as cursor:
        sql = "DELETE from `products` where id=%s"
        cursor.execute(sql, ID)
        connection.commit()
    return resp_data


# [POST方法]根据id更新状态项目状态，做软删除
@app_product.route("/api/product/remove", methods=['POST'])
def product_remove():
    resp_data = {
        "code": 20000,
        "message": "success",
        "data": []
    }
    id = request.args.get('id')
    if id is None:
        resp_data["code"] = 20002
        resp_data["message"] = "请求ID参数为空"
        return resp_data
    connection = connectDB()
    with connection.cursor() as cursor:
        sql = 'update `products` set status=1 where id=%s;'
        cursor.execute(sql, id)
        connection.commit()
    return resp_data


# 搜索接口
@app_product.route("/api/product/search", methods=['GET'])
def product_search():
    # 获取title和keyCode
    title = request.args.get('title')
    keyCode = request.args.get('keyCode')

    # 基础语句定义
    sql = "SELECT * FROM `products` WHERE `status`=0"

    # 如果title不为空，拼接tilite的模糊查询
    if title is not None:
        sql = sql + " AND `title` LIKE '%{}%'".format(title)
    # 如果keyCode不为空，拼接tilite的模糊查询
    if keyCode is not None:
        sql = sql + " AND `keyCode` LIKE '%{}%'".format(keyCode)

    # 排序最后拼接
    sql = sql + " ORDER BY `update` DESC"

    connection = connectDB()
    # 使用python的with..as控制流语句（相当于简化的try except finally）
    with connection.cursor() as cursor:
        # 按照条件进行查询
        print(sql)
        cursor.execute(sql)
        data = cursor.fetchall()

    # 按返回模版格式进行json结果返回
    resp_data = {
        "code": 20000,
        "data": data
    }

    return resp_data
