# -*- coding:utf-8 -*-
# testmanager.py

from flask import Blueprint
from dbutils.pooled_db import PooledDB
from config import config, format

from flask import request
import pymysql.cursors
import json

from utils.email_tools import sendEmail

# 使用数据库连接池的方式链接数据库，提高资源利用率
pool = PooledDB(pymysql, mincached=4, maxcached=10, host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor,blocking=True)
connection = pool.connection()
test_manager = Blueprint("test_manager", __name__)


@test_manager.route("/api/test/search", methods=['POST'])
def searchBykey():
    body = request.get_data()
    body = json.loads(body)

    # 基础语句定义
    sql = ""

    # 获取pageSize和
    pageSize = 10 if 'pageSize' not in body or body['pageSize'] is None else body['pageSize']
    currentPage = 1 if 'currentPage' not in body or body['currentPage'] is None else body['currentPage']

    # 拼接查询条件
    if 'productId' in body and body['productId'] != '':
        sql = sql + " AND A.productId LIKE '%{}%'".format(body['productId'])
    if 'appId' in body and body['appId'] != '':
        sql = sql + " AND A.appId LIKE '%{}%'".format(body['appId'])
    if 'tester' in body and body['tester'] != '':
        sql = sql + " AND R.tester LIKE '%{}%'".format(body['tester'])
    if 'developer' in body and body['developer'] != '':
        sql = sql + " AND R.developer LIKE '%{}%'".format(body['developer'])
    if 'status' in body and body['status'] != '':
        sql = sql + " AND R.status = '{}'".format(body['status'])
    if 'pickTime' in body and body['pickTime']:
        sql = sql + " AND R.updateDate >= '{}' and R.updateDate <= '{}' ".format(body['pickTime'][0],
                                                                                 body['pickTime'][1])

    # 排序和页数拼接
    sql = sql + ' ORDER BY R.updateDate DESC LIMIT {},{}'.format((currentPage - 1) * pageSize, pageSize)

 
        # 先查询总数
    print(sql)
    with connection.cursor() as cursor:
        count_select = 'SELECT COUNT(*) as `count` FROM request as R , apps as A where R.appId = A.id AND R.isDel=0' + sql
        print(count_select)
        cursor.execute(count_select)
        total = cursor.fetchall()

    # 执行查询
    with connection.cursor() as cursor:
        # 按照条件进行查询
        data_select = 'SELECT A.appId,R.* FROM request as R , apps as A where R.appId = A.id AND R.isDel=0' + sql
        # print(data_select)
        cursor.execute(data_select)
        data = cursor.fetchall()

    # 按分页模版返回查询数据
    response = format.resp_format_success
    response['data'] = data
    response['total'] = total[0]['count']
    return response


@test_manager.route("/api/test/create", methods=['POST'])
def createReqeust():
    # 获取传递的数据，并转换成JSON
    body = request.get_json()

    # 定义默认返回体
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    # 判断必填参数
    if 'appId' not in body:
        resp_failed['message'] = 'appId 提测应用不能为空'
        return resp_failed
    elif 'tester' not in body:
        resp_failed['message'] = 'tester 测试人员不能为空'
        return resp_failed
    elif 'developer' not in body:
        resp_failed['message'] = 'developer 提测人不能为空'
        return resp_failed
    elif 'title' not in body:
        resp_failed['message'] = 'title提测标题不能为空'
        return resp_failed
    if body['isEmail'] == 'true':
        # 新建成功发送Email
        if body['type'] == '1':
            version = '功能测试'
        elif body['type'] == '2':
            version = '性能测试'
        elif body['type'] == '3':
            version = '安全测试'

        receivers = body["tester"].split(',') + body["developer"].split(',')
        if not body["CcMail"] is None:
            receivers = receivers + body["CcMail"].split(',')

        subject = '【提测】' + body['title']
        reuslt = sendEmail(receivers, subject, [
            '<strong>[提测应用]</strong>',
            body['appName'],
            '<strong>[提测人]</strong>',
            body['developer'],
            '<strong>[提测版本]</strong>',
            body['version'],
            '<strong>[提测类型]</strong>',
            version,
            '<strong>[测试内容]</strong>',
            body['scope'],
            '<strong>[相关文档]</strong>',
            body['wiki'],
            '<strong>[补充信息]</strong>',
            body['more']
        ])
        if reuslt:
            sendOk = 1
        else:
            sendOk = 2
        print(body["appId"])
        with connection.cursor() as cursor:
            # 更新Emai是否发送成功1-成功 2-失败
            updateEmail = "UPDATE request SET sendEmail=%s, updateUser=%s,`updateDate`= NOW() WHERE id=%s"
            cursor.execute(updateEmail, (sendOk, body["updateUser"], body["appId"]))
            # 提交修改邮件是否发送成功
            connection.commit()
    else:
        print('不发送邮件！')
    # 使用连接池链接数据库

    # 判断增加或是修改逻辑

    try:
        with connection.cursor() as cursor:
            # 拼接插入语句,并用参数化%s构造防止基本的SQL注入
            # 其中id为自增，插入数据默认数据设置的当前时间
            sqlInsert = "INSERT INTO request (title,appId,developer,tester,CcMail,version,`type`,scope,gitCode,wiki,`more`,`status`,createUser,updateUser) " \
                        "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cursor.execute(sqlInsert, (
                body["title"], body["appId"], body["developer"], body["tester"], body["CcMail"], body["version"],
                body['type'],
                body["scope"], body["gitCode"], body["wiki"], body["more"], '1', body["createUser"],
                body["updateUser"]))
            # 提交执行保存新增数据
            id = cursor.lastrowid
            connection.commit()
        return resp_success
    except Exception as err:
        resp_failed['message'] = '提测失败了:' + err
        return resp_failed


@test_manager.route("/api/test/info", methods=['GET'])
def getTestInfo():
    print(request)
    test_id = request.args.get('id')
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    if not test_id:

        resp_failed.message = '提测ID不能为空'

        return resp_failed

    with connection.cursor() as cursor:

        # 查询产品信息表-按更新时间新旧排序

        sql = "SELECT A.id as appId, A.appId as appName, R.id,R.title,R.developer,R.tester,R.CcMail,R.version,R.type,R.scope,R.gitCode,R.wiki,R.more FROM request as R , apps as A where R.appId = A.id AND R.isDel=0 AND R.id={}".format(test_id)
        print(sql)
        cursor.execute(sql)

        data = cursor.fetchall()

        if len(data) == 1:

            resp_success['data'] = data[0]

    return resp_success


@test_manager.route("/api/test/update", methods=['POST'])
def updateReqeust():
    '''...请求值获取，返回值，参数判断部分省略....'''
    resp_success=format.resp_format_success
    body=request.get_json()
        # 先将历史数据查出来备用
    with connection.cursor() as cursor:
        sql = "SELECT A.appId as appId, A.note as appName, R.id,R.title,R.developer,R.tester,R.CcMail,R.version,R.type,R.scope,R.gitCode,R.wiki,R.more FROM request as R , apps as A where R.appId = A.id AND R.isDel=0 AND R.id={}".format(

            body['id'])
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) == 1:
            old_test_info = data[0]
        else:
            print('原有数据请求查询异常！')
        # 如果传的值有ID，那么进行修改操作，否则为新增数据
        with connection.cursor() as cursor:
            # 拼接修改语句，由于应用名不可修改，不需要做重复校验appId
            sqlUpdate = "UPDATE request SET title=%s,appId=%s,developer=%s,tester=%s,CcMail=%s,version=%s,`type`=%s, scope=%s,gitCode=%s,wiki=%s,`more`=%s,updateUser=%s,`updateDate`= NOW() WHERE id=%s"
            cursor.execute(sqlUpdate, (
                body["title"], body["appId"], body["developer"], body['tester'], body["CcMail"], body["version"],
                body["type"], body["scope"], body["gitCode"], body["wiki"], body["more"], body["updateUser"],
                body["id"]))
            # 提交执行保存更新数据
            connection.commit()
            # 更新需要发送邮件的化需要进行是否有更改对比
            if 'isEail' in body and body['isEmail'] == 'true':

                # 新建成功发送Email
                if body['type'] == 1:
                    rquest_type = '功能测试'
                elif body['type'] == 2:
                    rquest_type = '性能测试'
                elif body['type'] == 3:
                    rquest_type = '安全测试'
                receivers = body["tester"].split(',') + body["developer"].split(',')
                if not body["CcMail"] is None:
                    receivers = receivers + body["CcMail"].split(',')
                subject = '【提测】' + body['title']
                contents = []
                contents.append('<strong>[提测应用]</strong>')
                if old_test_info and old_test_info['appName'] != body['appName']:
                    contents.append(old_test_info['appName'] + '变更为:' + body['appName'])
                else:
                    contents.append(body['appName'])
                contents.append('<strong>[提测人]</strong>')
                if old_test_info and old_test_info['developer'] != body['developer']:
                    contents.append(old_test_info['developer'] + '变更为:' + body['developer'])
                else:
                    contents.append(body['developer'])
                contents.append('<strong>[提测版本]</strong>')
                if old_test_info and old_test_info['version'] != body['version']:
                    contents.append(old_test_info['version'] + '变更为:' + body['version'])
                else:
                    contents.append(body['developer'])
                contents.append('<strong>[测试内容]</strong>')
                if old_test_info and old_test_info['scope'] != body['scope']:
                    contents.append(old_test_info['scope'] + '变更为:' + body['scope'])
                else:
                    contents.append(body['scope'])
                contents.append('<strong>[相关文档]</strong>')
                if old_test_info and old_test_info['wiki'] != body['wiki']:
                    contents.append(old_test_info['wiki'] + '变更为:' + body['wiki'])
                else:
                    contents.append(body['wiki'])
                contents.append('<strong>[补充信息]</strong>')
                if old_test_info and old_test_info['more'] != body['more']:
                    contents.append(old_test_info['more'] + '变更为:' + body['more'])
                else:
                    contents.append(body['more'])
                reuslt = sendEmail(receivers, subject,contents)
                if reuslt:
                    sendOk = 1
                else:
                    sendOk = 2

                with connection.cursor() as cursor:
                    # 更新Emai是否发送成功1-成功 2-失败
                    updateEmail = "UPDATE request SET sendEmail=%s, updateUser=%s,`updateDate`= NOW() WHERE id=%s"
                    cursor.execute(updateEmail, (sendOk, body["updateUser"], body['id']))
                    # 提交修改邮件是否发送成功
                    connection.commit()
            else:
                print('不发送邮件！')
    return resp_success


@test_manager.route("/api/test/change", methods=['POST'])
def changeStatus():

    # 初始化返回对象
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed
    # 获取请求参数Body
    reqbody = request.get_json()
    if 'id' not in reqbody:
        resp_failed['message'] = '提测ID不能为空'
        return resp_failed
    elif 'status' not in reqbody:
        resp_failed['message'] = '更改的状态不能为空'
        return resp_failed
    # 重新链接数据库
    with connection.cursor() as cursor:
        # 判断状态流转的操作，如果status==start为开始测试，status==delete 软删除
        if reqbody['status'] == 'start':
            sql = "UPDATE `request` SET `status`=2 WHERE id=%s"
            resp_success['message'] = '状态流转成功，进入测试阶段。'
        elif reqbody['status'] == 'delete':
            sql = "UPDATE `request` SET `isDel`=1 WHERE id=%s"
            resp_success['message'] = '提测已被删除!'
        else:
            resp_failed.message = '状态标记错误'
            return resp_failed
        cursor.execute(sql, reqbody['id'])
        connection.commit()
    return resp_success

import os
# 涉及的相关依赖引用
from wtforms import Form,FileField
from flask_wtf.file import FileRequired,FileAllowed
from werkzeug.utils import secure_filename
from werkzeug.datastructures import CombinedMultiDict
# 表单提交相关校验
class fileForm(Form):
    file = FileField(validators=[FileRequired(), FileAllowed(['jpg', 'png', 'gif', 'pdf', 'zip'])])

@test_manager.route("/api/report/upload",methods=['POST'])
def uploadFile():
    # 初始化返回对象
    resp_success = format.resp_format_success
    resp_failed = format.resp_format_failed

    file_form = fileForm(CombinedMultiDict([request.form, request.files]))
    if file_form.validate():
        # 获取项目路径+保存文件夹，组成服务保存绝对路径
        save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('service')[0], 'service/static')
        # 通过表单提交的form-data获取选择上传的文件
        attfile = request.files.get('file')
        # 进行安全名称检查处理
        file_name = secure_filename(attfile.filename)
        # 保存文件文件中
        attfile.save(os.path.join(save_path, file_name))

        resp_success['data'] = {"fileName": file_name}
        return resp_success
    else:
        resp_failed['message'] = '文件格式不符合预期'
        return resp_failed
    
from flask import send_from_directory
@test_manager.route("/api/file/download",methods=['GET'])
def downloadFile():
    fimeName = request.args.get('name')
    # 保存文件的相对路径
    save_path = os.path.join(os.path.abspath(os.path.dirname(__file__)).split('service')[0], 'service/static')
    result = send_from_directory(save_path, fimeName)
    return  result