import json

from dbutils.pooled_db import PooledDB
import pymysql.cursors
from flask import Blueprint, request

from config import config,format
from applications.exts import db
from applications.models.products import ProductsModule
from applications.models.apps import AppsModel
from sqlalchemy import func,and_
from sqlalchemy.orm import joinedload
app_application = Blueprint("app_application", __name__, url_prefix="/api/application")
    # 定义默认返回体
resp_success = format.resp_format_success
resp_failed = format.resp_format_failed

@app_application.route("/product", methods=["GET"])
def get_products():
    """
    :return:返回分类数据
    """
    data_table=db.session.query(ProductsModule.id,ProductsModule.keyCode,ProductsModule.title,
                                ).filter(ProductsModule.status==0).order_by(ProductsModule.update.desc()).all()
    data=[{'id': item.id, 'keyCode': item.keyCode, 'title': item.title} for item in data_table]

    resp_success['data'] = data
    return resp_success 


@app_application.route("/search", methods=['POST'])
def searchBykey():
    body = request.get_json()
   
    # 获取pageSize和
    pageSize = body.get('pageSize',10)
    currentPage = body.get('currentPage',1)
    del  body['pageSize']
    del  body['currentPage']
    filter_conditions = []
    # 拼接查询条件
    fields_to_check = {  
    'productId': AppsModel.productId == body['productId'],  # 不使用LIKE  
    'appId': AppsModel.appId.like(body['appId']),  
    'note': AppsModel.note.like(body['note']),  
    'tester': AppsModel.tester.like(body['tester']),  
    'developer': AppsModel.developer.like(body['developer']),  
    'producer': AppsModel.producer.like(body['producer']),  
}


# 遍历body字典并添加条件到filter_conditions列表中  
    for key, value in body.items():
        if key in fields_to_check and value.strip() != '':  
            if key == 'productId':  # 对于productId，不使用LIKE，直接使用等号
                filter_conditions.append(fields_to_check[key].replace(body[key], value))  
            else:  
                # 对于其他字段，使用LIKE，并替换%作为通配符  
                filter_conditions.append(fields_to_check[key].replace(body[key], '%' + value + '%'))

    query= db.session.query(func.count(ProductsModule.id)).filter(AppsModel.productId == ProductsModule.id,  AppsModel.status == 0)
   
    if filter_conditions:
        query = query.filter(and_(*filter_conditions))
    # 查询总数
    total = query.scalar()
    query= db.session.query(AppsModel.id,
                            AppsModel.productId,
                            AppsModel.note,
                            AppsModel.developer,
                            AppsModel.producer,
                            AppsModel.tester,
                            AppsModel.updateUser,
                            AppsModel.updateDate,
                            ProductsModule.title
                            ).filter(AppsModel.productId == ProductsModule.id,  AppsModel.status == 0,AppsModel.isDel==0)

    apps_data = query.all()
    apps_data=[{'appId':item.id,
                'productId':item.productId,
                'note':item.note,
                'developer':item.developer,
                'tester':item.tester,
                'producer':item.producer,
                'updateUser':item.updateUser,
                'updateDate':item.updateDate,
                'title':item.title,
                } for item in apps_data]
    # 按分页模版返回查询数据
    resp_success['data'] = apps_data
    resp_success['total'] = total
    return resp_success

@app_application.route("/update", methods=['POST'])
def product_update():
    # 获取传递的数据，并转换成JSON
    body = request.get_json()
    # 判断必填参数
    fail_message_dict={
        'appId': '应用不能为空',
        'tester': '测试负责人不能为空',
        'developer': '研发负责人不能为空',
        'producer': '产品负责人不能为空',
        'cCEmail': 'cCEmail不能为空',
    }
    empty_value_keys = [key for key, value in body.items() if value == '']  
    if empty_value_keys and fail_message_dict.get(empty_value_keys[0],None):
        resp_failed['message'] = fail_message_dict[empty_value_keys[0]]
        return  resp_failed
    key_id = body.get('appId', None)
    print(body)
    print(key_id)
    if key_id:
        '''
        判断增加或是修改逻辑
        如果传的值有ID，那么进行修改操作，否则为新增数据
        '''
        db.session.query(AppsModel).filter(AppsModel.id ==body['appId']).update(
            {
                'productId':body["productId"],'note':body["note"],'tester':body["note"],
                'developer':body["developer"],'producer':body["developer"],'CcEmail':body["cCEmail"], 
                'gitCode':body["gitCode"], 'wiki':body["wiki"], 'more':body["more"], 
                'createUser':body["createUser"],'updateUser':body["updateUser"]})
        db.session.commit()
        
    else:
        # 新增需要判断appId是否重复
        result=db.session.query(AppsModel).filter(AppsModel.id ==body['appId'],AppsModel.status==0).filter()
        #有数据说明存在相同值，封装提示直接返回
        if result:
            resp_failed["code"] = 20001
            resp_failed["message"] = "唯一编码keyCode已存在"
            return resp_failed

        # 拼接插入语句,并用参数化%s构造防止基本的SQL注入
        # 其中id为自增，插入数据默认数据设置的当前时间
        add_app=AppsModel(
            appId=body["appId"],
            productId=body["productId"],
            note=body["note"],
            tester=body["tester"],
            producer=body["producer"],
            gitCode=body["gitCode"],
            wiki=body["wiki"],
            more=body["more"],
            creteUser=body["creteUser"],
            updateUser=body["updateUser"],
            
                  )
         # 提交执行保存新增数据
        db.session.add(add_app)
        db.session.commit()
           
        return resp_success

@app_application.route("/options", methods=['GET'])
def getOptionsForSelected():

    value = request.args.get('value', '')
    response = format.resp_format_success

    connection = pool.connection()

    with connection.cursor() as cursor:

        # 先按appid模糊搜索，没有数据再按note搜索
        sqlByAppId = "SELECT * FROM apps WHERE appId LIKE '%"+value+"%'"
        cursor.execute(sqlByAppId)
        dataByppId = cursor.fetchall()
        if len(dataByppId) > 0 :
            response['data'] = dataByppId
        else:
            sqlByNote = "SELECT * FROM apps WHERE note LIKE '%" + value + "%'"
            cursor.execute(sqlByNote)
            dataByNote = cursor.fetchall()
            response['data'] = dataByNote

    return response