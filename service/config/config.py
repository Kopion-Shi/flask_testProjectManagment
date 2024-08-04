# config.py
#
import datetime

PORT = 5000
DEBUG = True
SECRET_KEY = "Zpf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
JWT_SECRET_KEY = "Zpf9Wkove4IKEAXvy-cQkeDPhv9Cb3Ag-wyJILbq_dFw"
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=1)
# Bcrypt is set as default SECURITY_PASSWORD_HASH, which requires a salt
# Generate a good salt using: secrets.SystemRandom().getrandbits(128)
SECURITY_PASSWORD_SALT = "146585145368132386173505678016728509634"

# have session and remember cookie be samesite (flask/flask_login)
REMEMBER_COOKIE_SAMESITE = "strict"
SESSION_COOKIE_SAMESITE = "strict"
SECURITY_TRACKABLE = True
# mysql数据库配置
MYSQL_HOST = "localhost"
MYSQL_PORT = 3306
MYSQL_DATABASE = "tpmstore"
MYSQL_USER = "root"
MYSQL_PASSWORD = "123456"

##mogondb
MONGODB_SETTINGS = {
    "db": "tpmstore",
    "host": "localhost",
    "port": 10001,
    "connect": True,
    "username": "admin",
    "password": "123456",
}
##smpt服务地址
EMAIL_HOST = "smtp.qq.com"
EMAIL_PORT = 465
# 发送邮件的邮箱，需要配置开通SMTP
EMAIL_HOST_USER = "1694348126@qq.com"
# 在邮箱中设置的客户端授权密码
# 此处的EMAIL_HOST_PASSWORD是用QQ邮箱授权码登录,不难，请自行百度
EMAIL_HOST_PASSWORD = "bdyaqmrjcfcpfcjj"
# 收件人看到的发件人
EMAIL_FROM = "weblei<1694348126@qq.com>"
SQLALCHEMY_DATABASE_URI = f"mysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DATABASE}?unix_socket=/var/run/mysqld/mysqld.sock"
SQLALCHEMY_RECORD_QUERIES = True

MAX_CONTENT_LENGTH = 16 * 1000 * 1000

FLASK_ADMIN_SWATCH = "cerulean"
