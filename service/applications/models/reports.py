from service.applications.exts import db
from sqlalchemy import func


class ReportModules(db.Model):
    __tablename__ = 'report'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, 
                   nullable=False, unique=True, comment="主键ID")
    
    createDate= db.Column(db.DateTime, comment="创建时间")
    updataDate= db.Column(db.DateTime, comment="更新时间")
    
    updateUser=db.Column(db.String(20),comment="修改人")
    test_desc=db.Column(db.String(2000),comment="结论描述")
    test_risks=db.Column(db.String(2000),comment="风险提示")
    test_cases=db.Column(db.String(2000),comment="测试用例描述")
    test_bugs=db.Column(db.String(1000),comment="缺陷列表")
    test_file=db.Column(db.String(255),comment="附件文件地址")
    test_note=db.Column(db.String(1000),comment="报告备注")
    test_email=db.Column(db.String(1),comment="修改是否发送消息，0未操作，1成功，2失败人")

    
    def __repr__(self):  
        return f"<report(id={self.id})>" 