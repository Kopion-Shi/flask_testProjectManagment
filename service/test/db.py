# import pymysql.cursors
# from dbutils.pooled_db import PooledDB

# from service.config import config

# pool = PooledDB(pymysql, mincached=2, maxcached=5, host=config.MYSQL_HOST, port=config.MYSQL_PORT,
#                 user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE,
#                 cursorclass=pymysql.cursors.DictCursor)
# connection = pool.connection()
# with connection.cursor() as cursor:
#     for i in range(999999):

#         sql = "INSERT INTO `products` (`keyCode`,`title`,`desc`,`operator`) VALUES (%s, %s, %s, %s)"
#         print(i)
#         cursor.execute(sql, (f'keyCode_{i}', f'title_{i}', f'desc_{i}', 'operator_{i}'))
#         connection.commit()

body={'id': '', 'appId': 10000, 'productId': 5, 'note': '', 'tester': 'Carl3633524461@outlook.com', 'developer': 'Carl3633524461@outlook.com', 'producer': 'Carl3633524461@outlook.com', 'cCEmail': '', 'gitCode': '', 'wiki': '', 'more': '', 'creteUser': 'Super Admin', 'updateUser': 'Super Admin'}
fail_message_dict={
    'appId': '应用不能为空',
    'tester': '测试负责人不能为空',
    'developer': '研发负责人不能为空',
    'producer': '产品负责人不能为空',
}
fail_message=list(filter(lambda item:item not in fail_message_dict,body))
print(fail_message)
