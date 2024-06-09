# config.py
# mysql数据库配置
MYSQL_HOST = 'localhost'
MYSQL_PORT = 3306
MYSQL_DATABASE = 'tpmstore'
MYSQL_USER = 'root'
MYSQL_PASSWORD = '123456'

##
MONGODB_DB = 'tpmstore'
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

##smpt服务地址
EMAIL_HOST = 'smtp.qq.com'
EMAIL_PORT = 465
# 发送邮件的邮箱，需要配置开通SMTP
EMAIL_HOST_USER = '1694348126@qq.com'
# 在邮箱中设置的客户端授权密码
# 此处的EMAIL_HOST_PASSWORD是用QQ邮箱授权码登录,不难，请自行百度
EMAIL_HOST_PASSWORD = 'bdyaqmrjcfcpfcjj'
# 收件人看到的发件人
EMAIL_FROM = 'weblei<1694348126@qq.com>'
SQLALCHEMY_DATABASE_URI=f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?unix_socket=/var/run/mysqld/mysqld.sock"
SQLALCHEMY_RECORD_QUERIES=False

MAX_CONTENT_LENGTH = 16 * 1000 * 1000
SECRET_KEY="ZtAaJjHk8K"