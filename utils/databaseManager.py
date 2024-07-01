from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Sequence, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import NullPool, QueuePool
from contextlib import contextmanager

Base = declarative_base()


class AdminUser(Base):
    __tablename__ = 'admin_user'  # 管理员
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), nullable=False)
    hash = Column(String(70), nullable=False)  # 存储密码,pssql存储过长是由于byte字节导致的
    updatetime = Column(DateTime, nullable=True, default=datetime.utcnow() + timedelta(hours=8))  # 存储变更时间


class AdminLog(Base):
    __tablename__ = 'admin_login_log'  # 登录日志
    id = Column(Integer, primary_key=True, autoincrement=True)
    ip = Column(String(100), nullable=False)
    updatetime = Column(DateTime, nullable=True, default=datetime.utcnow() + timedelta(hours=8))  # 存储变更时间


class Payment(Base):
    __tablename__ = 'payment'  # 支付
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # 支付接口名称
    icon = Column(String(100), nullable=False)  # 图标
    config = Column(Text)  # 配置参数{}json
    info = Column(String(100))  # 描述
    isactive = Column(Boolean, nullable=False, default=False)


class ProdCag(Base):
    __tablename__ = 'prod_cag'  # 分类设置
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # 名称
    info = Column(String(100), nullable=False, comment='描述')  # 描述
    sort = Column(Integer, nullable=True, default=1000)  # 排序id


class ProdInfo(Base):
    __tablename__ = 'prod_info'  # 产品信息
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    # cag_name = Column(String(50),ForeignKey('prod_cag.name'))  #关联后，无法update或删除
    cag_name = Column(String(50))  # 关联测试
    name = Column(String(150), nullable=False, unique=True)  #
    info = Column(String(150), nullable=True)  # 产品一句话描述
    img_url = Column(String(150), nullable=True)  # 主图
    sort = Column(Integer, nullable=True, default=1000)  # 排序
    discription = Column(Text, nullable=True)  # 完整描述
    price = Column(Float, nullable=False)  # 价格
    price_wholesale = Column(String(150), nullable=True)  # 折扣
    # iswholesale = Column(Text, nullable=False,default=False)  #是否启用折扣
    auto = Column(Boolean, nullable=False, default=False)  # 手工或自动发货
    sales = Column(Integer, nullable=True, default=0)  # 销量
    tag = Column(String(50), nullable=True, default='优惠折扣')  # 标签
    isactive = Column(Boolean, nullable=False, default=False)  # 激活为1


class Order(Base):
    __tablename__ = 'order'  # 订单信息
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    out_order_id = Column(String(50), nullable=False)  # 订单ID
    name = Column(String(50), nullable=False)  # 商品名
    payment = Column(String(50), nullable=False)  # 支付渠道
    contact = Column(String(50))  # 联系方式
    contact_txt = Column(Text, nullable=True)  # 附加信息
    price = Column(Float, nullable=False)  # 价格
    num = Column(Integer, nullable=False)  # 数量
    total_price = Column(Float, nullable=False)  # 总价
    card = Column(Text, nullable=True)  # 卡密
    status = Column(Boolean, nullable=True, default=True)  # 订单状态
    updatetime = Column(DateTime, nullable=False)  # 交易时间


class TempOrder(Base):
    # 临时订单信息---商品名称或ID+订单号+数量+支付方式+联系方式+备注；时间信息---》推算价格---》支付状态---》付款【名称、订单号、数量、价格】
    __tablename__ = 'temporder'
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    out_order_id = Column(String(50), nullable=False)  # 订单ID
    name = Column(String(50), nullable=False)  # 商品名
    payment = Column(String(50), nullable=False)  # 支付渠道
    contact = Column(String(50))  # 联系方式
    contact_txt = Column(Text, nullable=True)  # 附加信息
    price = Column(Float, nullable=False)  # 价格--推算步骤
    num = Column(Integer, nullable=False)  # 数量
    total_price = Column(Float, nullable=False)  # 总价--推算步骤
    status = Column(Boolean, nullable=True, default=True)  # 订单状态---False
    auto = Column(Boolean, nullable=False, default=False)  # 手工或自动发货
    updatetime = Column(DateTime, nullable=False, default=datetime.utcnow() + timedelta(hours=8))  # 创建时间
    endtime = Column(DateTime, nullable=True)  # 最后时间


class Order2(Base):
    __bind_key__ = 'order'  # 使用order数据库
    __tablename__ = 'order2'  # 订单信息
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    out_order_id = Column(String(50), nullable=False)  # 订单ID
    name = Column(String(50), nullable=False)  # 商品名
    payment = Column(String(50), nullable=False)  # 支付渠道
    contact = Column(String(50))  # 联系方式
    contact_txt = Column(Text, nullable=True)  # 附加信息
    price = Column(Float, nullable=False)  # 价格
    num = Column(Integer, nullable=False)  # 数量
    total_price = Column(Float, nullable=False)  # 总价
    card = Column(Text, nullable=True)  # 卡密
    status = Column(Boolean, nullable=True, default=True)  # 订单状态
    updatetime = Column(DateTime, nullable=False)  # 交易时间


class Card(Base):
    __tablename__ = 'card'  # 卡密
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    prod_name = Column(String(50), nullable=False)  # 商品ID
    card = Column(Text, nullable=False)  # 卡密
    reuse = Column(Boolean, nullable=True, default=False)  # 是否重复使用
    isused = Column(Boolean, nullable=True, default=False)  # 是否已用


class Config(Base):
    __tablename__ = 'config'  # 系统配置
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False, unique=True)  # 变量名
    info = Column(Text, nullable=True)  # 值
    description = Column(Text, nullable=False)  # 描述
    isshow = Column(Boolean, nullable=False, default=False)  # 描述
    updatetime = Column(DateTime, nullable=True, default=datetime.utcnow() + timedelta(hours=8))  # 交易时间


class Plugin(Base):
    __tablename__ = 'plugin'  # 通知或文章存档
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # 微信公众号+Tg发卡
    config = Column(Text, nullable=False)  # 配置参数{}json
    about = Column(Text, nullable=False)  # 关于或联系页面
    switch = Column(Boolean, nullable=False)  # 开关0/1;true,false


class Notice(Base):
    __tablename__ = 'notice'  # 通知引擎
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)  # 邮箱、微信、TG、短信
    config = Column(Text, nullable=False)  # 配置参数{}json
    admin_account = Column(String(100), nullable=False, default=False)  # 150000
    admin_switch = Column(Boolean, nullable=True, default=False)  # 管理员开关
    user_switch = Column(Boolean, nullable=True, default=False)  # 用户开关


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text, nullable=False)
    password = Column(Text, nullable=False)


"""
代码说明：
基础配置：
Base 是 SQLAlchemy 的基类，用于所有 ORM 模型。
User 是一个示例模型，用于演示数据库操作。
"""


class Database:
    """__init__ 方法初始化数据库连接。
       create_tables 方法创建数据库表。
       drop_tables 方法删除数据库表。
       session_scope 提供一个事务范围，以确保数据库操作的原子性和一致性。
       add_sample_data 方法插入样例数据。
       add_record 方法添加记录。
       get_record 方法获取单条记录。
       get_all_records 方法获取所有记录。
       update_record 方法更新记录。
       delete_record 方法删除记录。
       clear_table 方法清空表。
       switch_database 方法切换数据库。
       使用方法：
       实例化 Database 类并传入数据库 URL。
       调用 create_tables 方法创建表。
       使用其他方法进行增删改查操作。
       使用 switch_database 方法切换到其他数据库。
    """

    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = self._create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def _create_engine(self, db_url):
        if 'sqlite' in db_url:
            return create_engine(db_url, echo=True, poolclass=NullPool)
        else:
            return create_engine(db_url, echo=True, pool_size=20, max_overflow=0)

    def create_tables(self):
        """创建数据库表"""
        Base.metadata.create_all(self.engine)

    def create_example_data(self):
        """创建示例数据"""
        with self.session_scope() as session:
            # 管理员信息
            session.add(AdminUser(email='admin@qq.com', hash='$2b$12$BKSXKYuCgeXjr8IEbK02re0VhkFoAz7f3aHF3kYAMLzYaEiObqPYm'))

            # 邮箱配置
            # session.add(Smtp('demo@qq.com', '卡密发卡网', 'smtp.qq.com', '465', 'xxxxxxxxx', True))

            # 支付渠道
            session.add(Payment(name='支付宝当面付', icon='支付宝', config="{'APPID':'2016091800537528','alipay_public_key':'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4AHTfGleo8WI3qb+mSWOjJRyn6Vh8XvO6YsQmJjPnNKhvACHTHcU+PCUWUKZ54fSVhMkFZEQWMtAGeOt3lGy3pMBS96anh841gxJc2NUljU14ESXnDn4QdVe4bosmYvfko46wfA0fGClHdpO8UUiJGLj1W5alv10CwiCrYRDtx93SLIuQgwJn4yBC1/kE/KENOaWaA45dXIQvKh2P0lTbm0AvwYMVvYB+eB1GtOGQbuFJXUxWaMa0byTo9wSllhgyiIkOH+HJ9oOZIweGlsrezeUUdr3EEX97k25LdnUt/oQK8FIfthexfWZpTDDlHqmI7p6gCtRVDJenU4sxwpEyQIDAQAB','app_private_key':'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCqWmxsyPLwRmZHwoLYlUJXMF7PATKtvp7BrJfwLbxwrz6I48G11HpPPyAoNynwAMG7DCXjVX76NCbmfvvPqnbk09rNRULqGju8G6NkQTbLfDjhJs+CE8kdIs89btxqDG70ebePiZTGpQngPLfrziKDOhRfXkA5qRPImbC+PUXiXq9qvkp9Yu/8IYjyxUpNBNjZuTK+fTjSI0RCt7eE+wR0KqpNIzot1q/ds1KTIYmJQM5tEFie4BK0pDtGiIs/VrUG8PTPqLyzEyIMy1N75olUWAiGrk0USqiieP3TYj0PdlQDX2T14DOwMkl5Rjvt7Knc+WGdolPIBssUX1wTE+J7AgMBAAECggEAWpRP+Jv0yRu1wMxFRKJArxmSH+GUL9wej/6Un2nCO+yChMkNtAAxtLdtAtUqIGpWmH2CG9nW9XULhh3ZCPer1kprmiAMz2t5fbD4dRNT7miz2cwIJDMfCbX7mb+7xUutJ6Mcnl7aU7FnierfJKvrn/ke4gK8haxIT66g0tbDtPQhYnGPawyM+gqFulaMBcuqH0naAIq5ZBWHkKuuwJ1SD6yGrWgHdq3Kt2pE8b9yjfdUl15IeW0rszXG6fTika9WX6qaulyoGAAZdjiXED+mbRyqZA3jq7RI38qBP9+/jAb+fdwE8EwqnpPvfGHMBdkREOXK0kzRU8rpd9GbH7INaQKBgQDwpuW+bK/qxKx3BSAXL98f0J2I7YVuk0EFCStGoxnzWRv0yvL0QEDwN+QPiVMmcVQcr79mW5zTBkd4vmr3ud+v1f/X6UPI82kQhZlVWry8LEnisPlZuE0E/EaJrLgF7z4l3ItzCVi8IfpgizPcCYSz/vY49a5W34eKjXHWUB1jDwKBgQC1N8PgGKI2LRDaJeqt5Ef6yyYSMOgVe0WSqAlgyMECb1pjmMBjcNG1AFE/FfgNu4thOaXIogElGVoQFvA5GuJQY48HOJNgx3Ua2SxiowcXkAN0gIm4FY+ozkp7xhizvLVfsmX+MKqPtl6nggiWETJJyvMQnjMgKLmSvhsopMwZ1QKBgGV36az2BOK3VITGq3Y7YBf5DUN76uPpwOOPryiUgs+hhfEcVX55TSg8WLPYUjAGXtHNpKVTAXfU0PPvTgjv3Yo1cC+okkU7pNQrkLB1lti8z9Z+ilSzKf5tJIzOP7V437p1GHNDwJ9qsDhe2VnwxXxjh4wSwxSsIWlhJFuZ4hovAoGAFgm8Fmqof3InlH/79D3IyyUdciTkdIhTQ6yPx2dioYstMOOIsg8sUZjCSKvBSNo/7wj1slqRTROyMja37Bnq39/bqwMkWSaohSVYEn7FBAaNhQOEvBBTMjI0OK00n9cZL5QgdzMv6t5A0JottSJOPU8jFChJC2Yoe0IHR4ATGikCgYB2smi7/ptKiGdwmiuUHsF/U3jfjpHyHwLrXjoSU+mwV+GjqcdbtkSP1suGjN8tcdbFvLSCRX/IRdFHYJeuPUXQtZtiC431+upasbEiJ1xZ2KcK3lKf0mOn10kPD5QC7mmsfmjz4cw9cSrBjmcWGXeIwIXPLhOAAIzpHqy8oP/F/g=='}", info='alipay.com 官方接口0.38~0.6%', isactive=True))
            session.add(Payment(name='微信官方接口', icon='微信支付', config="{'APPID':'XXXXXXXX','MCH_ID':'XXXXXX','APP_SECRET':'XXXXXX'}", info='pay.weixin.qq.com 微信官方0.38%需要营业执照', isactive=False))
            session.add(Payment(name='QQ钱包', icon='QQ支付', config="{'mch_id':'XXXXXXXX','key':'YYYYY'}", info='mp.qpay.tenpay.com QQ官方0.6%需要营业执照', isactive=False))
            session.add(Payment(name='虎皮椒支付宝', icon='支付宝', config="{'API':'api.vrmrgame.com','appid':'XXXXXX','AppSecret':'YYYYY'}", info='xunhupay.com 个人接口0.38%+1~2%', isactive=False))
            session.add(Payment(name='虎皮椒微信', icon='微信支付', config="{'API':'api.vrmrgame.com','appid':'XXXXXX','AppSecret':'YYYYY'}", info='xunhupay.com 个人接口0.38~0.6%+1~2%', isactive=False))
            session.add(Payment(name='PAYJS支付宝', icon='支付宝', config="{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}", info='payjs.cn 个人接口2.38%', isactive=False))
            session.add(Payment(name='PAYJS微信', icon='微信支付', config="{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}", info='payjs.cn 个人接口2.38%', isactive=False))
            session.add(Payment(name='迅虎微信', icon='微信支付', config="{'ID':'XXXXXX','Key':'YYYYY',}", info='pay.xunhuweb.com 个人接口0.38~0.6%+1~2%', isactive=False))   # https://admin.xunhuweb.com/pay/payment 返回系统异常错误
            session.add(Payment(name='码支付支付宝', icon='支付宝', config="{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}", info='codepay.fateqq.com[不可用]', isactive=False))
            session.add(Payment(name='码支付微信', icon='微信支付', config="{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}", info='codepay.fateqq.com[不可用]', isactive=False))
            session.add(Payment(name='码支付QQ', icon='QQ支付', config="{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}", info='codepay.fateqq.com[不可用]', isactive=False))
            session.add(Payment(name='V免签支付宝', icon='支付宝', config="{'API':'http://google.com','KEY':'YYYYYYYY'}", info='0费率实时到账', isactive=False))
            session.add(Payment(name='V免签微信', icon='微信', config="{'API':'http://google.com','KEY':'YYYYYYYY'}", info='0费率实时到账', isactive=False))
            session.add(Payment(name='云免签支付宝', icon='支付宝', config="{'APP_ID':'XXXX','KEY':'YYYYYYYY'}", info='云端监控yunmianqian.com', isactive=False))
            session.add(Payment(name='云免签微信', icon='微信', config="{'APP_ID':'XXXX','KEY':'YYYYYYYY'}", info='云端监控yunmianqian.com', isactive=False))
            session.add(Payment(name='易支付QQ', icon='QQ支付', config="{'API':'http://google.com','ID':'XXXXX','KEY':'YYYYYYYY'}", info='任意一家易支付 高费率不稳定', isactive=False))
            session.add(Payment(name='易支付支付宝', icon='支付宝', config="{'API':'http://google.com','ID':'XXXXX','KEY':'YYYYYYYY'}", info='任意一家易支付高费率不稳定', isactive=False))
            session.add(Payment(name='易支付微信', icon='微信', config="{'API':'http://google.com','ID':'XXXXX','KEY':'YYYYYYYY'}", info='任意一家易支付 高费率不稳定', isactive=False))
            session.add(Payment(name='YunGouOS', icon='微信或支付宝支付', config="{'mch_id':'xxxxxx','pay_secret':'yyyyyyy'}", info='yungouos.com 微信或支付宝个体1+0.38%', isactive=False))
            session.add(Payment(name='YunGouOS_WXPAY', icon='微信支付', config="{'mch_id':'xxxxxx','pay_secret':'yyyyyyy'}", info='yungouos.com 微信个体1+0.38~0.6%', isactive=False))
            session.add(Payment(name='Mugglepay', icon='Mugglepay', config="{'TOKEN':'xxxxxx','Currency':'CNY'}", info='mugglepay.com全球综合收款系统(已修复)', isactive=False))
            session.add(Payment(name='Stripe支付宝', icon='支付宝', config="{'key':'sk_xxx','currency':'cny'}", info='stripe.com综合收款系统(已完成逻辑，但未实测,缺少反馈)', isactive=False))
            session.add(Payment(name='Stripe微信', icon='微信支付', config="{'key':'sk_xxx','currency':'usd'}", info='stripe.com综合收款系统(aud, cad, eur, gbp, hkd, jpy, sgd, usd)', isactive=False))

            # 商品分类
            session.add(ProdCag(name='账户ID', info='虚拟账号类商品', sort='100'))
            session.add(ProdCag(name='激活码', info='单独激活类商品', sort='1000'))
            session.add(ProdCag(name='第三分类', info='单独激活类商品', sort='1000'))

            # 商品设置
            session.add(ProdInfo(cag_name='账户ID', name='普通商品演示', info='商品简述信息演示XXXX', img_url='images/null.png', sort='100', discription='示例：卡密格式：账号------密码-----', price=9.99, price_wholesale=None, auto=True, sales=0, tag='请填写邮箱', isactive=True))
            # session.add(ProdInfo(cag_name='账户ID', name='批发商品演示', info='商品简述信息演示XXXX', img_url='images/null.png', sort='100', discription='示例：我是商品描述信息-', price=9.99, price_wholesale='9,100#9.9,8.82,7.7'None, auto=True, sales=0,tag=0,isactive=True))
            session.add(ProdInfo(cag_name='账户ID', name='批发商品演示', info='商品简述信息演示XXXX', img_url='images/null.png', sort='100', discription='示例：卡密格式：账号------密码-----', price=9.99, price_wholesale=None, auto=True, sales=0, tag='请填写邮箱', isactive=True))
            session.add(ProdInfo(cag_name='账户ID', name='普通商品DD', info='商品简述信息演示XXXX', img_url='images/null.png', sort='100', discription='示例：卡密格式：账号------密码-----', price=9.99, price_wholesale=None, auto=False, sales=0, tag='请填写邮箱', isactive=False))
            session.add(ProdInfo(cag_name='激活码', name='重复卡密演示', info='商品简述信息演示XXXX', img_url='images/null.png', sort='100', discription='示例：卡密格式：账号------密码-----', price=9.99, price_wholesale=None, auto=True, sales=0, tag='请填写邮箱', isactive=True))
            session.add(ProdInfo(cag_name='激活码', name='普通商品CC', info='商品简述信息演示XXXX', img_url='images/null.png', sort='100', discription='示例：卡密格式：账号------密码-----', price=9.99, price_wholesale=None, auto=True, sales=0, tag='请填写邮箱', isactive=True))
            session.add(ProdInfo(cag_name='激活码', name='普通商品BB', info='商品简述信息演示XXXX', img_url='images/null.png', sort='100', discription='示例：卡密格式：账号------密码-----', price=9.99, price_wholesale=None, auto=True, sales=0, tag='请填写邮箱', isactive=False))

            # 卡密设置
            session.add(Card(prod_name='普通商品演示', card='454545454454545454', reuse=False, isused=False))
            session.add(Card(prod_name='批发商品演示', card='555555555555555555', reuse=False, isused=False))
            session.add(Card(prod_name='批发商品演示', card='666666666666666666', reuse=False, isused=False))
            session.add(Card(prod_name='重复卡密演示', card='666666666666666666', reuse=True, isused=False))

            # 系统配置
            session.add(Config(name='web_name', info='KAMIFAKA', description='网站名称', isshow=True))
            session.add(Config(name='web_keyword', info='关键词、收录词汇', description='网站关键词', isshow=True))
            session.add(Config(name='description', info='网站描述信息。。。', description='网站描述', isshow=True))
            session.add(Config(name='web_url', info='http://localhost:80', description='必填，网站实际地址', isshow=True))
            session.add(Config(name='web_bg_url', info='https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/colorfull.jpg', description='网站背景图片', isshow=True))
            session.add(Config(name='contact_us', info='<p>示例，请在管理后台>>网站设置里修改，支持HTML格式</p>', description='首页-联系我们', isshow=True))
            session.add(Config(name='web_footer', info='<a style="color: #fafafa;" href="https://www.baidu.com">川ICP备1101XXXX号-10</a>', description='可填写备案信息', isshow=True))
            session.add(Config(name='top_notice', info='稳定版演示站点，公告信息可在后台设置', description='首页公告', isshow=True))
            session.add(Config(name='toast_notice', info='稳定版演示站点，公告信息可在后台设置', description='首页滑动消息设置', isshow=True))
            # session.add(Config(name='top_notice', info='开发版演示站点，公告信息可在后台设置', description='首页公告', isshow=True))
            # session.add(Config(name='toast_notice', info='这里是开发板，每天更新好几次那种', description='首页滑动消息设置', isshow=True))
            # session.add(Config(name='modal_notice', info='【计划中】','全局弹窗信息', isshow=True))
            session.add(Config(name='contact_option', info='0', description='是否启用联系方式查询[0启用，1关闭]', isshow=True))
            session.add(Config(name='theme', info='list', description='主题', isshow=False))
            session.add(Config(name='kamiFaka', info='https://www.baidu.com', description='Github项目地址，用于手动检测新版', isshow=False))
            session.add(Config(name='kamiFaka_v', info='1.88', description='Github项目地址，用于手动检测新版', isshow=False))

            # 通知渠道 ：名称；对管理员开关；对用户开关；对管理员需要管理员账号；用户无；名称+config+管理员+admin_switch+user_switch
            session.add(Notice(name='邮箱通知', config="{'sendname':'no_replay','sendmail':'demo@gmail.com','smtp_address':'smtp.163.com','smtp_port':'465','smtp_pwd':'ZZZZZZZ'}", admin_account='demo@qq.com', admin_switch=False, user_switch=False))
            session.add(Notice(name='微信通知', config="{'token':'AT_nvlYDjev89gV96hBAvUX5HR3idWQwLlA'}", admin_account='xxxxxxxxxxxxxxxx', admin_switch=False, user_switch=False))
            session.add(Notice(name='TG通知', config="{'TG_TOKEN':'1290570937:AAHaXA2uOvDoGKbGeY4xVIi5kR7K55saXhs'}", admin_account='445545444', admin_switch=False, user_switch=False))
            session.add(Notice(name='短信通知', config="{'username':'XXXXXX','password':'YYYYY','tokenYZM':'必填','templateid':'必填'}", admin_account='15347875415', admin_switch=False, user_switch=False))
            session.add(Notice(name='QQ通知', config="{'Key':'null'}", admin_account='格式：您的KEY@已添加的QQ号,示例：abc@123', admin_switch=False, user_switch=False))

            # 订单信息【测试环境】
            session.add(Order(out_order_id='演示订单可删除', name='普通商品演示', payment='支付宝当面付', contact='472835979', contact_txt='请求尽快发货', price=9.99, num=1, total_price=0.9, card='账号：xxxxx；密码：xxxx', status=None, updatetime=None))
            session.add(Order(out_order_id='演示订单可删除2', name='普通商品演示', payment='虎皮椒微信', contact='458721@qq.com', contact_txt='非常感谢', price=9.99, num=3, total_price=1.97, card=None, status=None, updatetime=None))  # 卡密为None或‘’空都可以
            session.add(Order(out_order_id='Order_1608107857954q7kyldyg', name='普通商品演示', payment='虎皮椒支付宝', contact='demo@gmail.com', contact_txt='不错', price=9.99, num=1, total_price=0.9, card='此处为卡密', status=None, updatetime=None))
            session.add(Order(out_order_id='演示订单4457', name='普通商品演示', payment='虎皮椒支付宝', contact='472835979', contact_txt='不错', price=9.99, num=1, total_price=1.9, card='TG卡密DEMO', status=None, updatetime=None))

            # 插件配置信息
            session.add(Plugin(name='TG发卡', config="{'TG_TOKEN':'1488086653:AAHihuO0JuvmiDNZtsYcDBpUhL1rTDO6o1C'}", about='### 示例 \n请在管理后台--》Telegram里设置，支持HTML格式', switch=False))
            session.add(Plugin(name='微信公众号', config="{'PID':'xxxxxxxxxxxx'}", about='<p>示例，请在管理后台>>Telegram里设置，支持HTML格式</p>', switch=False))

            # 临时订单
            session.add(TempOrder(out_order_id='id44454', name='重复卡密演示', payment='alipay', contact='154311', contact_txt='', price=10, status=False, updatetime=None))
            session.add(TempOrder(out_order_id='id44454', name='批发商品演示', payment='alipay', contact='154311', contact_txt='', price=22, status=False, updatetime=None))


    def drop_tables(self):
        """删除数据库表"""
        Base.metadata.drop_all(self.engine)

    @contextmanager
    def session_scope(self):
        """提供一个事务范围"""
        session = self.Session()
        try:
            yield session
            session.commit()
        except SQLAlchemyError as e:
            session.rollback()
            print(f"Error occurred: {e}")
        finally:
            session.close()

    def add_record(self, record):
        """添加记录"""
        with self.session_scope() as session:
            session.add(record)

    def get_record(self, model, record_id):
        """获取记录"""
        with self.session_scope() as session:
            return session.query(model).filter_by(id=record_id).first()

    def get_all_records(self, model):
        """获取所有记录"""
        with self.session_scope() as session:
            return session.query(model).all()

    def update_record(self, model, record_id, **kwargs):
        """更新记录"""
        with self.session_scope() as session:
            record = session.query(model).filter_by(id=record_id).first()
            for key, value in kwargs.items():
                setattr(record, key, value)
            session.add(record)

    def delete_record(self, model, record_id):
        """删除记录"""
        with self.session_scope() as session:
            record = session.query(model).filter_by(id=record_id).first()
            session.delete(record)

    def clear_table(self, model):
        """清空表"""
        with self.session_scope() as session:
            session.query(model).delete()

    def switch_database(self, new_db_url):
        """切换数据库"""
        self.db_url = new_db_url
        self.engine = self._create_engine(new_db_url)
        self.Session = sessionmaker(bind=self.engine)


# 示例用法
if __name__ == "__main__":
    db = Database('sqlite:///database.db')  # 使用 SQLite 数据库
    db.create_tables()

    db.create_example_data()

    # 测试插入示例数据
    db.add_record(User(username="admin", password="admin"))
    # 测试查询示例数据
    with db.session_scope() as session:
        user = session.query(User).filter_by(id=1).first()
        print(f"Retrieved User: {user.username}, {user.password}")
    # 测试更新示例数据
    db.update_record(User, 1, username="admin", password="123")
    # 测试获取所有示例数据
    with db.session_scope() as session:
        users = session.query(User).all()
        for user in users:
            print(f"User: {user.username}, {user.password}")
    # # 测试删除示例数据
    # db.delete_record(User, 1)
    # # 测试清空示例数据
    # db.clear_table(User)
    # # 测试删除数据库
    # db.drop_tables()
