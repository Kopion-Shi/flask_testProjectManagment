from service.applications.exts import sqlAlchemy_db as db
from sqlalchemy import func


class RequestModel(db.Model):
    __tablename__ = "request"
    id = db.Column(db.Integer, autoincrement=True, primary_key=True, nullable=False, comment="自增id")

    title = db.Column(db.String(200), comment="提测标题")
    appId = db.Column(db.String(50), comment="应用服务")
    developer = db.Column(db.String(255), comment="提测RD")
    tester = db.Column(db.String(255), comment="测试QA")
    CcMail = db.Column(db.String(500), comment="关系人")
    version = db.Column(db.String(100), comment="关系人",
                        info={'collation': 'utf8mb4_0900_ai_ci'})
    type = db.Column(db.Integer, comment="提测类型 1.功能 2.性能 3.安全")
    scope = db.Column(db.Text, comment="测试说明")
    gitCode = db.Column(db.String(200), comment="项目代码")
    wiki = db.Column(db.String(200), comment="产品文档")
    more = db.Column(db.Text, comment="是否发送邮件，0未操作，1成功，2失败")
    status = db.Column(db.Integer, comment="测试状态 1-已提测 2-测试中 3-通过 4-失败 9-废弃")
    sendEmail = db.Column(db.Integer, comment="是否发送消息，0未操作，1成功，2失败")
    isDel = db.Column(db.Integer, default=0, comment="状态0正常1删除")

    createUser = db.Column(db.String(20), nullable=True,
                           # Flask-SQLAlchemy 不直接支持 collation，但你可以在这里存储元数据  
                           info={'collation': 'utf8mb4_0900_ai_ci'},
                           comment='创建人')
    createDate = db.Column(db.DateTime, nullable=False, server_default=func.now(), comment='创建时间')
    updateUser = db.Column(db.String(20), nullable=True,
                           # Flask-SQLAlchemy 不直接支持 collation，但你可以在这里存储元数据  
                           info={'collation': 'utf8mb4_0900_ai_ci'},
                           comment='修改人')
    updateDate = db.Column(db.DateTime, nullable=False, server_default=func.now(), onupdate=func.now(),
                           comment='修改时间')
    test_desc = db.Column(db.String(2000), comment="结论描述")
    test_risks = db.Column(db.String(2000), comment="风险提示")
    test_cases = db.Column(db.String(2000), comment="测试用例描述")
    test_bugs = db.Column(db.String(1000), comment="缺陷列表")
    test_file = db.Column(db.String(255), comment="附件文件地址")
    test_note = db.Column(db.String(1000), comment="结论报告备注描述")
    test_email = db.Column(db.Integer, default=0, comment="是否发送消息，0未操作，1成功，2失败")

    def __repr__(self):
        return f"<request(id={self.id})>"
