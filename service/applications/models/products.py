from applications.exts import db
from sqlalchemy import func


class ProductsModule(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                   nullable=False, unique=True, comment="编号自增")
    keyCode=db.Column(db.String(200),nullable=False,comment="项目唯一编号")
    title=db.Column(db.String(200),nullable=False,comment="中文项目名")
    desc=db.Column(db.String(500),nullable=False,comment="中文项目名",default='',
                    info={'collation': 'utf8mb4_0900_ai_ci'})
    status=db.Column(db.Integer,nullable=False,default=0,comment="状态",
                     info={'collation': 'utf8mb4_0900_ai_ci'})
    operator=db.Column(db.String(50),nullable=False,comment="操作者")
    update=db.Column(db.DateTime,nullable=False,server_default=func.now(), 
                     onupdate=func.now(),comment="操作时间")
    
    def __repr__(self):  
        return f"<products(id={self.id})>" 