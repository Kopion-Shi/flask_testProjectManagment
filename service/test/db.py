import pymysql.cursors
from dbutils.pooled_db import PooledDB

from service.config import config

pool = PooledDB(pymysql, mincached=2, maxcached=5, host=config.MYSQL_HOST, port=config.MYSQL_PORT,
                user=config.MYSQL_USER, passwd=config.MYSQL_PASSWORD, database=config.MYSQL_DATABASE,
                cursorclass=pymysql.cursors.DictCursor)
connection = pool.connection()
with connection.cursor() as cursor:
    for i in range(999999):

        sql = "INSERT INTO `products` (`keyCode`,`title`,`desc`,`operator`) VALUES (%s, %s, %s, %s)"
        print(i)
        cursor.execute(sql, (f'keyCode_{i}', f'title_{i}', f'desc_{i}', 'operator_{i}'))
        connection.commit()
