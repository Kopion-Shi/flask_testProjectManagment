# -*- coding:utf-8 -*-
import pymysql.cursors
from flask import Blueprint

app_product = Blueprint("app_product", __name__)

connection = pymysql.connect(host='localhost', user='root', password='root', database='tpmstore', charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app_product.route("/api/product/list", methods=["GET"])
def product_list():
    # 硬编码返回list
    with connection.cursor() as cursor:
        sql = "select * from Products ORDER BY 'UPDATE' DESC;"
        cursor.execute(sql)
        data = cursor.fetchall()
    # 按返回模版格式进行json结果返回
    resp_data = {"code": 20000, "data": data}

    return resp_data
