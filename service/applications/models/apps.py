from service.applications.exts import db
from sqlalchemy import func
from sqlalchemy.schema import UniqueConstraint  
class AppsModel(db.Model):
    __tablename__="apps"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False,comment="自增id")
    appId = db.Column(db.String(50), nullable=True,comment="应用服务ID")
    productId = db.Column(db.Integer, nullable=True,comment="外键关联产品所属")
    note = db.Column(db.String(100), nullable=True,comment="应用描述")
    tester = db.Column(db.String(300), nullable=True,comment="测试负责人")
    developer = db.Column(db.String(300), nullable=True,comment="默认研发负责人")
    producer = db.Column(db.String(300), nullable=True,comment="默认产品经理")
    CcEmail = db.Column(db.String(500), nullable=True,comment="默认抄送邮件或组")
    gitCode = db.Column(db.String(200), nullable=True,comment="代码地址")
    wiki = db.Column(db.String(200), nullable=True,comment="项目说明地址")
    more = db.Column(db.Text, comment="默认产品经理")
    status = db.Column(db.Integer, default=0, nullable=False, comment='提测状态：1-已提测 2-测试中 3-通过 4-失败 9-废弃')
    isDel = db.Column(db.Integer, default=0, nullable=False, comment='状态0正常1删除')
    createUser = db.Column(db.String(20), nullable=True, default=None,  
                           # Flask-SQLAlchemy 不直接支持 collation，但你可以在这里存储元数据  
                           info={'collation': 'utf8mb4_0900_ai_ci'},  
                           comment='创建人') 
    createDate = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updateUser = db.Column(db.String(20), nullable=True, default=None,  
                           # Flask-SQLAlchemy 不直接支持 collation，但你可以在这里存储元数据  
                           info={'collation': 'utf8mb4_0900_ai_ci'},  
                           comment='修改人') 
    updateDate = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(), comment='修改时间') 
    _table_args__ = (UniqueConstraint('id', name='apps_id_uindex'),)   
  
    def __repr__(self):  
        return f"<apps(id={self.id})>"  
