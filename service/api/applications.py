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
'''
{'code': 20000, 'message': 'success', 'data': [{'title': '22', 'id': 20015, 'appId': '2', 'productId': 13, 'note': '2', 'tester': '1', 'developer': '1', 'producer': '1', 'CcEmail': '1', 'gitCode': '', 'wiki': '', 'more': '', 'status': '0', 'creteUser': '', 'createDate': datetime.datetime(2024, 3, 14, 22, 21, 22), 'updateUser': 'Super Admin', 'updateDate': datetime.datetime(2024, 3, 16, 15, 52, 30)}, {'title': '22', 'id': 20018, 'appId': '11', 'productId': 13, 'note': '', 'tester': '1', 'developer': '1', 'producer': '1', 'CcEmail': '1', 'gitCode': '', 'wiki': '', 'more': '', 'status': '0', 'creteUser': '', 'createDate': datetime.datetime(2024, 3, 16, 15, 37, 53), 'updateUser': 'Super Admin', 'updateDate': datetime.datetime(2024, 3, 16, 15, 44, 34)}, {'title': '22', 'id': 20017, 'appId': '22', 'productId': 13, 'note': '1', 'tester': '1', 'developer': '1', 'producer': '1', 'CcEmail': '', 'gitCode': '1', 'wiki': '', 'more': '', 'status': '0', 'creteUser': '', 'createDate': datetime.datetime(2024, 3, 16, 15, 37), 'updateUser': 'Super Admin', 'updateDate': datetime.datetime(2024, 3, 16, 15, 37)}, {'title': '22', 'id': 20016, 'appId': '5', 'productId': 13, 'note': '1', 'tester': '1', 'developer': '5', 'producer': '5', 'CcEmail': '1', 'gitCode': '5', 'wiki': '5', 'more': '', 'status': '0', 'creteUser': '', 'createDate': datetime.datetime(2024, 3, 16, 15, 9, 29), 'updateUser': 'Super Admin', 'updateDate': datetime.datetime(2024, 3, 16, 15, 29, 56)}, {'title': '22', 'id': 20014, 'appId': '1', 'productId': 13, 'note': '1', 'tester': '1', 'developer': '1', 'producer': '1', 'CcEmail': '1', 'gitCode': '', 'wiki': '', 'more': '', 'status': '0', 'creteUser': '', 'createDate': datetime.datetime(2024, 3, 14, 22, 21, 10), 'updateUser': 'Super Admin', 'updateDate': datetime.datetime(2024, 3, 14, 22, 21, 10)}, {'title': '111', 'id': 15605, 'appId': '4koFhtMwxR', 'productId': 7, 'note': 'tScbNBB7wx', 'tester': 'KCVaOJkDN5', 'developer': 'RZqxdBCaaV', 'producer': 'QTChGofTPp', 'CcEmail': 'cdixon@yahoo.com', 'gitCode': 'JZXNGtPr3N', 'wiki': '2ld0NbZG23', 'more': 'Navicat Monitor requires a repository to store alerts and metrics for historical analysis. It collects process metrics such as CPU load, RAM usage, and a variety of other resources over SSH/SNMP. Secure SHell (SSH) is a program to log in into another computer over a network, execute commands on a remote server, and move files from one machine to another. The Synchronize to Database function will give you a full picture of all database differences. If the Show objects under schema in navigation pane option is checked at the Preferences window, all database objects are also displayed in the pane. Actually it is just in an idea when feel oneself can achieve and cannot achieve. With its well-designed Graphical User Interface(GUI), Navicat lets you quickly and easily create, organize, access and share information in a secure and easy way. To connect to a database or schema, simply double-click it in the pane. Remember that failure is an event, not a person. Sometimes you win, sometimes you learn. HTTP Tunneling is a method for connecting to a server that uses the same protocol (http://) and the same port (port 80) as a web server does. The Synchronize to Database function will give you a full picture of all database differences. Navicat Cloud could not connect and access your databases. By which it means, it could only store your connection settings, queries, model files, and virtual group; your database passwords and data (e.g. tables, views, etc) will not be stored to Navicat Cloud. The On Startup feature allows you to control what tabs appear when you launch Navicat. Secure SHell (SSH) is a program to log in into another computer over a network, execute commands on a remote server, and move files from one machine to another. Sometimes you win, sometimes you learn. It wasn’t raining when Noah built the ark. Sometimes you win, sometimes you learn. The reason why a great man is great is that he resolves to be a great man. If opportunity doesn’t knock, build a door. Remember that failure is an event, not a person. Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more.', 'status': 'r', 'creteUser': '3Uka3AfKdL', 'createDate': datetime.datetime(2018, 7, 31, 14, 33, 36), 'updateUser': '2021-10-04', 'updateDate': datetime.datetime(2023, 9, 19, 8, 51, 35)}, {'title': '111', 'id': 19358, 'appId': 'F8r8WlUkwi', 'productId': 7, 'note': '6unPsf9rzi', 'tester': 'yH7oyW1Lf2', 'developer': 'h1jjrfDfTN', 'producer': 'Vwso5C88wR', 'CcEmail': 'racurtis@gmail.com', 'gitCode': 'xgUNVbPp6N', 'wiki': 'TA2ebcLgeX', 'more': 'Navicat provides powerful tools for working with queries: Query Editor for editing the query text directly, and Query Builder, Find Builder or Aggregate Builder for building queries visually. Navicat 15 has added support for the system-wide dark mode. Export Wizard allows you to export data from tables, collections, views, or query results to any available formats.', 'status': 'd', 'creteUser': 'G4PWoVh93R', 'createDate': datetime.datetime(2017, 12, 18, 0, 5), 'updateUser': '2018-06-29', 'updateDate': datetime.datetime(2023, 6, 3, 9, 14, 48)}, {'title': '数据大盘', 'id': 20007, 'appId': 'hOmMpHzF8l', 'productId': 11, 'note': 'aGHgnAbpVi', 'tester': 'IWE3kIm6Lv', 'developer': 'lP9rrk30rt', 'producer': 'xg6a0G2aW7', 'CcEmail': 'chiuwaichoi@outlook.com', 'gitCode': 'Odt8i8kWIP', 'wiki': 'o86XoPSX8w', 'more': "Anyone who has never made a mistake has never tried anything new. Navicat authorizes you to make connection to remote servers running on different platforms (i.e. Windows, macOS, Linux and UNIX), and supports PAM and GSSAPI authentication. SQL Editor allows you to create and edit SQL text, prepare and execute selected queries. With its well-designed Graphical User Interface(GUI), Navicat lets you quickly and easily create, organize, access and share information in a secure and easy way. The reason why a great man is great is that he resolves to be a great man. To start working with your server in Navicat, you should first establish a connection or several connections using the Connection window. A comfort zone is a beautiful place, but nothing ever grows there. If your Internet Service Provider (ISP) does not provide direct access to its server, Secure Tunneling Protocol (SSH) / HTTP is another solution. With its well-designed Graphical User Interface(GUI), Navicat lets you quickly and easily create, organize, access and share information in a secure and easy way. Secure SHell (SSH) is a program to log in into another computer over a network, execute commands on a remote server, and move files from one machine to another. A query is used to extract data from the database in a readable format according to the user's request. Navicat Cloud provides a cloud service for synchronizing connections, queries, model files and virtual group information from Navicat, other Navicat family members, different machines and different platforms. In the middle of winter I at last discovered that there was in me an invincible summer. A comfort zone is a beautiful place, but nothing ever grows there. All the Navicat Cloud objects are located under different projects. You can share the project to other Navicat Cloud accounts for collaboration. It provides strong authentication and secure encrypted communications between two hosts, known as SSH Port Forwarding (Tunneling), over an insecure network. You will succeed because most people are lazy. After logged in the Navicat Cloud feature, the Navigation pane will be divided into Navicat Cloud and My Connections sections. Anyone who has never made a mistake has never tried anything new. The repository database can be an existing MySQL, MariaDB, PostgreSQL, SQL Server, or Amazon RDS instance. Sometimes you win, sometimes you learn. SQL Editor allows you to create and edit SQL text, prepare and execute selected queries. To successfully establish a new connection to local/remote server - no matter via SSL or SSH, set the database login information in the General tab. The Main Window consists of several toolbars and panes for you to work on connections, database objects and advanced tools. I will greet this day with love in my heart. A man is not old until regrets take the place of dreams. Always keep your eyes open. Keep watching. Because whatever you see can inspire you. You must be the change you wish to see in the world. Navicat Cloud provides a cloud service for synchronizing connections, queries, model files and virtual group information from Navicat, other Navicat family members, different machines and different platforms. Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more. In a Telnet session, all communications, including username and password, are transmitted in plain-text, allowing anyone to listen-in on your session and steal passwords and other information. Such sessions are also susceptible to session hijacking, where a malicious user takes over your session once you have authenticated. Navicat Data Modeler enables you to build high-quality conceptual, logical and physical data models for a wide variety of audiences. Export Wizard allows you to export data from tables, collections, views, or query results to any available formats. The first step is as good as half over. Genius is an infinite capacity for taking pains. The past has no power over the present moment. If opportunity doesn’t knock, build a door. All the Navicat Cloud objects are located under different projects. You can share the project to other Navicat Cloud accounts for collaboration. It can also manage cloud databases such as Amazon Redshift, Amazon RDS, Alibaba Cloud. Features in Navicat are sophisticated enough to provide professional developers for all their specific needs, yet easy to learn for users who are new to database server.", 'status': 'k', 'creteUser': '9vjIddUJSS', 'createDate': datetime.datetime(2023, 11, 27, 11, 27, 53), 'updateUser': '2013-03-07', 'updateDate': datetime.datetime(2023, 3, 2, 10, 22, 30)}, {'title': '111', 'id': 14608, 'appId': 'CKuXwusD3a', 'productId': 7, 'note': 'U9ymGhuHE0', 'tester': 'orIZDOTvSr', 'developer': 'IzHJvWb8QU', 'producer': 'bmPvNWl5bc', 'CcEmail': 'zhang806@outlook.com', 'gitCode': 'SVdnMBOdn1', 'wiki': 'S7608husSm', 'more': "Export Wizard allows you to export data from tables, collections, views, or query results to any available formats. I may not have gone where I intended to go, but I think I have ended up where I needed to be. In a Telnet session, all communications, including username and password, are transmitted in plain-text, allowing anyone to listen-in on your session and steal passwords and other information. To clear or reload various internal caches, flush tables, or acquire locks, control-click your connection in the Navigation pane and select Flush and choose the flush option. You must have the reload privilege to use this feature. Flexible settings enable you to set up a custom key for comparison and synchronization. The Information Pane shows the detailed object information, project activities, the DDL of database objects, object dependencies, membership of users/roles and preview. Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more. In a Telnet session, all communications, including username and password, are transmitted in plain-text, allowing anyone to listen-in on your session and steal passwords and other information. It collects process metrics such as CPU load, RAM usage, and a variety of other resources over SSH/SNMP. Monitored servers include MySQL, MariaDB and SQL Server, and compatible with cloud databases like Amazon RDS, Amazon Aurora, Oracle Cloud, Google Cloud and Microsoft Azure. The Navigation pane employs tree structure which allows you to take action upon the database and their objects through their pop-up menus quickly and easily. If the Show objects under schema in navigation pane option is checked at the Preferences window, all database objects are also displayed in the pane. After logged in the Navicat Cloud feature, the Navigation pane will be divided into Navicat Cloud and My Connections sections. A comfort zone is a beautiful place, but nothing ever grows there. A query is used to extract data from the database in a readable format according to the user's request. You can select any connections, objects or projects, and then select the corresponding buttons on the Information Pane. To connect to a database or schema, simply double-click it in the pane. All journeys have secret destinations of which the traveler is unaware. Creativity is intelligence having fun. Navicat authorizes you to make connection to remote servers running on different platforms (i.e. Windows, macOS, Linux and UNIX), and supports PAM and GSSAPI authentication. Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more. To successfully establish a new connection to local/remote server - no matter via SSL, SSH or HTTP, set the database login information in the General tab. Actually it is just in an idea when feel oneself can achieve and cannot achieve. The past has no power over the present moment.", 'status': 'D', 'creteUser': 'OGwYuWg8GI', 'createDate': datetime.datetime(2002, 9, 20, 11, 31, 9), 'updateUser': '2020-07-15', 'updateDate': datetime.datetime(2023, 2, 18, 23, 32, 1)}, {'title': '111', 'id': 19880, 'appId': 'ZSiCZppwJd', 'productId': 7, 'note': 'Edt0zgop3m', 'tester': 'OglbXfNtP4', 'developer': 'cAl2u3ctMM', 'producer': 'hcJ0RzOMJx', 'CcEmail': 'warren80@outlook.com', 'gitCode': 'c4pxfqhIxC', 'wiki': 'E7xGen55pY', 'more': "To connect to a database or schema, simply double-click it in the pane. There is no way to happiness. Happiness is the way. Navicat Data Modeler enables you to build high-quality conceptual, logical and physical data models for a wide variety of audiences. You will succeed because most people are lazy. It can also manage cloud databases such as Amazon Redshift, Amazon RDS, Alibaba Cloud. Features in Navicat are sophisticated enough to provide professional developers for all their specific needs, yet easy to learn for users who are new to database server. It collects process metrics such as CPU load, RAM usage, and a variety of other resources over SSH/SNMP. You can select any connections, objects or projects, and then select the corresponding buttons on the Information Pane. Navicat Cloud could not connect and access your databases. By which it means, it could only store your connection settings, queries, model files, and virtual group; your database passwords and data (e.g. tables, views, etc) will not be stored to Navicat Cloud. To open a query using an external editor, control-click it and select Open with External Editor. You can set the file path of an external editor in Preferences. Import Wizard allows you to import data to tables/collections from CSV, TXT, XML, DBF and more. The Navigation pane employs tree structure which allows you to take action upon the database and their objects through their pop-up menus quickly and easily. Export Wizard allows you to export data from tables, collections, views, or query results to any available formats. Monitored servers include MySQL, MariaDB and SQL Server, and compatible with cloud databases like Amazon RDS, Amazon Aurora, Oracle Cloud, Google Cloud and Microsoft Azure. Navicat Data Modeler enables you to build high-quality conceptual, logical and physical data models for a wide variety of audiences. How we spend our days is, of course, how we spend our lives. SSH serves to prevent such vulnerabilities and allows you to access a remote server's shell without compromising security. The Synchronize to Database function will give you a full picture of all database differences. You cannot save people, you can just love them. Anyone who has never made a mistake has never tried anything new. All the Navicat Cloud objects are located under different projects. You can share the project to other Navicat Cloud accounts for collaboration. Sometimes you win, sometimes you learn. The On Startup feature allows you to control what tabs appear when you launch Navicat. Navicat Cloud provides a cloud service for synchronizing connections, queries, model files and virtual group information from Navicat, other Navicat family members, different machines and different platforms. If opportunity doesn’t knock, build a door. Navicat is a multi-connections Database Administration tool allowing you to connect to MySQL, Oracle, PostgreSQL, SQLite, SQL Server, MariaDB and/or MongoDB databases, making database administration to multiple kinds of database so easy. Export Wizard allows you to export data from tables, collections, views, or query results to any available formats. The Navigation pane employs tree structure which allows you to take action upon the database and their objects through their pop-up menus quickly and easily. There is no way to happiness. Happiness is the way. In a Telnet session, all communications, including username and password, are transmitted in plain-text, allowing anyone to listen-in on your session and steal passwords and other information. It collects process metrics such as CPU load, RAM usage, and a variety of other resources over SSH/SNMP. Navicat authorizes you to make connection to remote servers running on different platforms (i.e. Windows, macOS, Linux and UNIX), and supports PAM and GSSAPI authentication. Navicat provides a wide range advanced features, such as compelling code editing capabilities, smart code-completion, SQL formatting, and more. It can also manage cloud databases such as Amazon Redshift, Amazon RDS, Alibaba Cloud. Features in Navicat are sophisticated enough to provide professional developers for all their specific needs, yet easy to learn for users who are new to database server. In other words, Navicat provides the ability for data in different databases and/or schemas to be kept up-to-date so that each repository contains the same information. HTTP Tunneling is a method for connecting to a server that uses the same protocol (http://) and the same port (port 80) as a web server does. A man’s best friends are his ten fingers. Navicat provides a wide range advanced features, such as compelling code editing capabilities, smart code-completion, SQL formatting, and more. How we spend our days is, of course, how we spend our lives. Sometimes you win, sometimes you learn. Navicat Data Modeler is a powerful and cost-effective database design tool which helps you build high-quality conceptual, logical and physical data models. If the plan doesn’t work, change the plan, but never the goal. If opportunity doesn’t knock, build a door. It can also manage cloud databases such as Amazon Redshift, Amazon RDS, Alibaba Cloud. Features in Navicat are sophisticated enough to provide professional developers for all their specific needs, yet easy to learn for users who are new to database server. Navicat Data Modeler is a powerful and cost-effective database design tool which helps you build high-quality conceptual, logical and physical data models. Navicat Cloud could not connect and access your databases. By which it means, it could only store your connection settings, queries, model files, and virtual group; your database passwords and data (e.g. tables, views, etc) will not be stored to Navicat Cloud. The reason why a great man is great is that he resolves to be a great man. SQL Editor allows you to create and edit SQL text, prepare and execute selected queries. Remember that failure is an event, not a person. If the Show objects under schema in navigation pane option is checked at the Preferences window, all database objects are also displayed in the pane. The Navigation pane employs tree structure which allows you to take action upon the database and their objects through their pop-up menus quickly and easily. Navicat authorizes you to make connection to remote servers running on different platforms (i.e. Windows, macOS, Linux and UNIX), and supports PAM and GSSAPI authentication. After logged in the Navicat Cloud feature, the Navigation pane will be divided into Navicat Cloud and My Connections sections. Sometimes you win, sometimes you learn. The Synchronize to Database function will give you a full picture of all database differences. If the Show objects under schema in navigation pane option is checked at the Preferences window, all database objects are also displayed in the pane. If you wait, all that happens is you get older. How we spend our days is, of course, how we spend our lives. Difficult circumstances serve as a textbook of life for people. Navicat allows you to transfer data from one database and/or schema to another with detailed analytical process. With its well-designed Graphical User Interface(GUI), Navicat lets you quickly and easily create, organize, access and share information in a secure and easy way. In a Telnet session, all communications, including username and password, are transmitted in plain-text, allowing anyone to listen-in on your session and steal passwords and other information. Navicat Data Modeler is a powerful and cost-effective database design tool which helps you build high-quality conceptual, logical and physical data models. Navicat Cloud provides a cloud service for synchronizing connections, queries, model files and virtual group information from Navicat, other Navicat family members, different machines and different platforms. Genius is an infinite capacity for taking pains.", 'status': 'r', 'creteUser': 'eqiZ6xoXN5', 'createDate': datetime.datetime(2011, 7, 12, 21, 18, 2), 'updateUser': '2007-07-22', 'updateDate': datetime.datetime(2022, 11, 4, 10, 26, 45)}], 'total': 52}

'''


@app_application.route("/update", methods=['POST'])
def product_update():
    # 获取传递的数据，并转换成JSON
    body = request.get_data()
    body = json.loads(body)
    print(body)
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
                    body["CcEmail"], body["gitCode"], body["wiki"], body["more"], body["creteUser"], body["updateUser"],
                    body["id"]))
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