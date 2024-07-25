from typing import TypeVar, List
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Text, Boolean, Float
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta
from sqlalchemy.future import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, desc
from contextlib import contextmanager
from utils.usersManager import User

T = TypeVar('T', bound=DeclarativeMeta)
Base = declarative_base()


class LoginLog(Base):
    __tablename__ = 'login_log'  # 登录日志
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
    sort = Column(Integer, nullable=False, default=100)  # 排序id
    state = Column(Boolean, nullable=False, default=False)  # 描述


class ProdInfo(Base):
    __tablename__ = 'prod_info'  # 产品信息
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(150), nullable=False, unique=True)  # 商品名称
    prod_cag_name = Column(String(50))  # 所属分类
    prod_info = Column(String(150), nullable=True)  # 产品一句话描述
    prod_img_url = Column(String(150), nullable=True)  # 主图
    prod_discription = Column(Text, nullable=True)  # 完整描述
    prod_price = Column(Float, nullable=False, default=888)  # 价格
    prod_price_wholesale = Column(String(150), nullable=True)  # 批发价格
    prod_sales = Column(Integer, nullable=True, default=0)  # 销量
    # iswholesale = Column(Text, nullable=False,default=False)  #是否启用折扣
    prod_tag = Column(String(50), nullable=True, default='优惠折扣')  # 产品标签
    auto = Column(Boolean, nullable=False, default=False)  # 手工或自动发货
    sort = Column(Integer, nullable=True, default=100)  # 排序
    state = Column(Boolean, nullable=False, default=False)  # 激活为1
    # 库存 查询数据库卡密数量


class Order(Base):
    __tablename__ = 'order'  # 订单信息
    __mapper_args__ = {'confirm_deleted_rows': False}
    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(Boolean, nullable=True, default=True)  # 订单状态
    out_order_id = Column(String(50), nullable=False)  # 订单ID
    name = Column(String(50), nullable=False)  # 商品名
    payment = Column(String(50), nullable=False)  # 支付渠道
    num = Column(Integer, nullable=False)  # 数量
    price = Column(Float, nullable=False)  # 价格
    # coupon = Column(String(50), nullable=True)  # TODO 优惠券
    total_price = Column(Float, nullable=False)  # 总价
    contact_txt = Column(Text, nullable=True)  # 附加信息
    updatetime = Column(DateTime, nullable=False, default=datetime.utcnow() + timedelta(hours=8))  # 存储当前时间
    contact = Column(String(50))  # 联系方式
    card = Column(Text, nullable=True)  # 卡密


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
       create_data 方法添加记录。
       read_data 方法获取单条记录。
       update_data 方法更新记录。
       delete_data 方法删除记录。
       get_all_records 方法获取所有记录。
       clear_table 方法清空表。
       switch_database 方法切换数据库。
       使用方法：
       实例化 Database 类并传入数据库 URL。
       调用 create_tables 方法创建表。
       使用其他方法进行增删改查操作。
       使用 switch_database 方法切换到其他数据库。
    """

    def __init__(self, db_url='sqlite:///database/database.db'):
        self.db_url = db_url
        self.engine = self._create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def _create_engine(self, db_url):
        if 'sqlite' in db_url:
            return create_engine(db_url, echo=True,
                                 # pool_size=5,
                                 # max_overflow=10,
                                 # connect_args={'check_same_thread': False, 'timeout': 10}
                                 )
        else:
            return create_engine(db_url, echo=True, pool_size=20, max_overflow=0)

    def create_tables(self):
        """创建数据库表"""
        Base.metadata.create_all(self.engine)

    def drop_tables(self):
        """删除数据库表"""
        Base.metadata.drop_all(self.engine)

    def clear_table(self, model):
        """清空表"""
        with self.session_scope() as session:
            session.query(model).delete()

    def switch_database(self, new_db_url):
        """切换数据库"""
        self.db_url = new_db_url
        self.engine = self._create_engine(new_db_url)
        self.Session = sessionmaker(bind=self.engine)

    def create_example_data(self):
        """创建示例数据"""
        print("=" * 100)
        # 邮箱配置
        # self.create_data(Smtp('demo@qq.com', '卡密发卡网', 'smtp.qq.com', '465', 'xxxxxxxxx', True))

        # 支付渠道
        self.create_data(Payment(name='支付宝当面付', icon='支付宝', config="{'APPID':'2016091800537528','alipay_public_key':'MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4AHTfGleo8WI3qb+mSWOjJRyn6Vh8XvO6YsQmJjPnNKhvACHTHcU+PCUWUKZ54fSVhMkFZEQWMtAGeOt3lGy3pMBS96anh841gxJc2NUljU14ESXnDn4QdVe4bosmYvfko46wfA0fGClHdpO8UUiJGLj1W5alv10CwiCrYRDtx93SLIuQgwJn4yBC1/kE/KENOaWaA45dXIQvKh2P0lTbm0AvwYMVvYB+eB1GtOGQbuFJXUxWaMa0byTo9wSllhgyiIkOH+HJ9oOZIweGlsrezeUUdr3EEX97k25LdnUt/oQK8FIfthexfWZpTDDlHqmI7p6gCtRVDJenU4sxwpEyQIDAQAB','app_private_key':'MIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCqWmxsyPLwRmZHwoLYlUJXMF7PATKtvp7BrJfwLbxwrz6I48G11HpPPyAoNynwAMG7DCXjVX76NCbmfvvPqnbk09rNRULqGju8G6NkQTbLfDjhJs+CE8kdIs89btxqDG70ebePiZTGpQngPLfrziKDOhRfXkA5qRPImbC+PUXiXq9qvkp9Yu/8IYjyxUpNBNjZuTK+fTjSI0RCt7eE+wR0KqpNIzot1q/ds1KTIYmJQM5tEFie4BK0pDtGiIs/VrUG8PTPqLyzEyIMy1N75olUWAiGrk0USqiieP3TYj0PdlQDX2T14DOwMkl5Rjvt7Knc+WGdolPIBssUX1wTE+J7AgMBAAECggEAWpRP+Jv0yRu1wMxFRKJArxmSH+GUL9wej/6Un2nCO+yChMkNtAAxtLdtAtUqIGpWmH2CG9nW9XULhh3ZCPer1kprmiAMz2t5fbD4dRNT7miz2cwIJDMfCbX7mb+7xUutJ6Mcnl7aU7FnierfJKvrn/ke4gK8haxIT66g0tbDtPQhYnGPawyM+gqFulaMBcuqH0naAIq5ZBWHkKuuwJ1SD6yGrWgHdq3Kt2pE8b9yjfdUl15IeW0rszXG6fTika9WX6qaulyoGAAZdjiXED+mbRyqZA3jq7RI38qBP9+/jAb+fdwE8EwqnpPvfGHMBdkREOXK0kzRU8rpd9GbH7INaQKBgQDwpuW+bK/qxKx3BSAXL98f0J2I7YVuk0EFCStGoxnzWRv0yvL0QEDwN+QPiVMmcVQcr79mW5zTBkd4vmr3ud+v1f/X6UPI82kQhZlVWry8LEnisPlZuE0E/EaJrLgF7z4l3ItzCVi8IfpgizPcCYSz/vY49a5W34eKjXHWUB1jDwKBgQC1N8PgGKI2LRDaJeqt5Ef6yyYSMOgVe0WSqAlgyMECb1pjmMBjcNG1AFE/FfgNu4thOaXIogElGVoQFvA5GuJQY48HOJNgx3Ua2SxiowcXkAN0gIm4FY+ozkp7xhizvLVfsmX+MKqPtl6nggiWETJJyvMQnjMgKLmSvhsopMwZ1QKBgGV36az2BOK3VITGq3Y7YBf5DUN76uPpwOOPryiUgs+hhfEcVX55TSg8WLPYUjAGXtHNpKVTAXfU0PPvTgjv3Yo1cC+okkU7pNQrkLB1lti8z9Z+ilSzKf5tJIzOP7V437p1GHNDwJ9qsDhe2VnwxXxjh4wSwxSsIWlhJFuZ4hovAoGAFgm8Fmqof3InlH/79D3IyyUdciTkdIhTQ6yPx2dioYstMOOIsg8sUZjCSKvBSNo/7wj1slqRTROyMja37Bnq39/bqwMkWSaohSVYEn7FBAaNhQOEvBBTMjI0OK00n9cZL5QgdzMv6t5A0JottSJOPU8jFChJC2Yoe0IHR4ATGikCgYB2smi7/ptKiGdwmiuUHsF/U3jfjpHyHwLrXjoSU+mwV+GjqcdbtkSP1suGjN8tcdbFvLSCRX/IRdFHYJeuPUXQtZtiC431+upasbEiJ1xZ2KcK3lKf0mOn10kPD5QC7mmsfmjz4cw9cSrBjmcWGXeIwIXPLhOAAIzpHqy8oP/F/g=='}", info='alipay.com 官方接口0.38~0.6%', isactive=True))
        self.create_data(Payment(name='微信官方接口', icon='微信支付', config="{'APPID':'XXXXXXXX','MCH_ID':'XXXXXX','APP_SECRET':'XXXXXX'}", info='pay.weixin.qq.com 微信官方0.38%需要营业执照', isactive=False))
        self.create_data(Payment(name='QQ钱包', icon='QQ支付', config="{'mch_id':'XXXXXXXX','key':'YYYYY'}", info='mp.qpay.tenpay.com QQ官方0.6%需要营业执照', isactive=False))
        self.create_data(Payment(name='虎皮椒支付宝', icon='支付宝', config="{'API':'api.vrmrgame.com','appid':'XXXXXX','AppSecret':'YYYYY'}", info='xunhupay.com 个人接口0.38%+1~2%', isactive=False))
        self.create_data(Payment(name='虎皮椒微信', icon='微信支付', config="{'API':'api.vrmrgame.com','appid':'XXXXXX','AppSecret':'YYYYY'}", info='xunhupay.com 个人接口0.38~0.6%+1~2%', isactive=False))
        self.create_data(Payment(name='PAYJS支付宝', icon='支付宝', config="{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}", info='payjs.cn 个人接口2.38%', isactive=False))
        self.create_data(Payment(name='PAYJS微信', icon='微信支付', config="{'payjs_key':'XXXXXX','mchid':'YYYYY','mchid':'ZZZZZZZ'}", info='payjs.cn 个人接口2.38%', isactive=False))
        self.create_data(Payment(name='迅虎微信', icon='微信支付', config="{'ID':'XXXXXX','Key':'YYYYY',}", info='pay.xunhuweb.com 个人接口0.38~0.6%+1~2%', isactive=False))   # https://admin.xunhuweb.com/pay/payment 返回系统异常错误
        self.create_data(Payment(name='码支付支付宝', icon='支付宝', config="{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}", info='codepay.fateqq.com[不可用]', isactive=False))
        self.create_data(Payment(name='码支付微信', icon='微信支付', config="{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}", info='codepay.fateqq.com[不可用]', isactive=False))
        self.create_data(Payment(name='码支付QQ', icon='QQ支付', config="{'codepay_id':'58027','codepay_key':'fgl454542WSDJHEJHDJZpTRrmbn','token':'jljCGU3pRvXXXXXXXXXXXb1iq'}", info='codepay.fateqq.com[不可用]', isactive=False))
        self.create_data(Payment(name='V免签支付宝', icon='支付宝', config="{'API':'http://google.com','KEY':'YYYYYYYY'}", info='0费率实时到账', isactive=False))
        self.create_data(Payment(name='V免签微信', icon='微信', config="{'API':'http://google.com','KEY':'YYYYYYYY'}", info='0费率实时到账', isactive=False))
        self.create_data(Payment(name='云免签支付宝', icon='支付宝', config="{'APP_ID':'XXXX','KEY':'YYYYYYYY'}", info='云端监控yunmianqian.com', isactive=False))
        self.create_data(Payment(name='云免签微信', icon='微信', config="{'APP_ID':'XXXX','KEY':'YYYYYYYY'}", info='云端监控yunmianqian.com', isactive=False))
        self.create_data(Payment(name='易支付QQ', icon='QQ支付', config="{'API':'http://google.com','ID':'XXXXX','KEY':'YYYYYYYY'}", info='任意一家易支付 高费率不稳定', isactive=False))
        self.create_data(Payment(name='易支付支付宝', icon='支付宝', config="{'API':'http://google.com','ID':'XXXXX','KEY':'YYYYYYYY'}", info='任意一家易支付高费率不稳定', isactive=False))
        self.create_data(Payment(name='易支付微信', icon='微信', config="{'API':'http://google.com','ID':'XXXXX','KEY':'YYYYYYYY'}", info='任意一家易支付 高费率不稳定', isactive=False))
        self.create_data(Payment(name='YunGouOS', icon='微信或支付宝支付', config="{'mch_id':'xxxxxx','pay_secret':'yyyyyyy'}", info='yungouos.com 微信或支付宝个体1+0.38%', isactive=False))
        self.create_data(Payment(name='YunGouOS_WXPAY', icon='微信支付', config="{'mch_id':'xxxxxx','pay_secret':'yyyyyyy'}", info='yungouos.com 微信个体1+0.38~0.6%', isactive=False))
        self.create_data(Payment(name='Mugglepay', icon='Mugglepay', config="{'TOKEN':'xxxxxx','Currency':'CNY'}", info='mugglepay.com全球综合收款系统(已修复)', isactive=False))
        self.create_data(Payment(name='Stripe支付宝', icon='支付宝', config="{'key':'sk_xxx','currency':'cny'}", info='stripe.com综合收款系统(已完成逻辑，但未实测,缺少反馈)', isactive=False))
        self.create_data(Payment(name='Stripe微信', icon='微信支付', config="{'key':'sk_xxx','currency':'usd'}", info='stripe.com综合收款系统(aud, cad, eur, gbp, hkd, jpy, sgd, usd)', isactive=False))

        # 商品分类
        self.create_data(ProdCag(name='账户ID', state=True, sort='100'))
        self.create_data(ProdCag(name='激活码', state=True, sort='100'))
        self.create_data(ProdCag(name='第三分类', state=True, sort='100'))

        # 商品
        self.create_data(ProdInfo(name='普通商品演示', prod_cag_name="账户ID", prod_info='商品简述信息演示XXXX', prod_img_url="prod_img_url", prod_discription="示例：卡密格式：账号------密码-----", prod_price=9.99, prod_price_wholesale=None, prod_sales=0, prod_tag="限时优惠", auto=True, sort='100', state=True))
        self.create_data(ProdInfo(name='普通商品演示', prod_cag_name="账户ID", prod_info='商品简述信息演示XXXX', prod_img_url="prod_img_url", prod_discription="示例：卡密格式：账号------密码-----", prod_price=9.99, prod_price_wholesale=None, prod_sales=0, prod_tag="限时优惠", auto=True, sort='100', state=True))
        self.create_data(ProdInfo(name='批发商品演示', prod_cag_name="账户ID", prod_info='商品简述信息演示XXXX', prod_img_url="images/null.png", prod_discription="示例：卡密格式：账号------密码-----", prod_price=9.99, prod_price_wholesale=None, prod_sales=0, prod_tag="限时优惠", auto=True, sort='100', state=True))
        self.create_data(ProdInfo(name='普通商品DD', prod_cag_name="账户ID", prod_info='商品简述信息演示XXXX', prod_img_url="images/null.png", prod_discription="示例：卡密格式：账号------密码-----", prod_price=9.99, prod_price_wholesale=None, prod_sales=0, prod_tag="限时优惠", auto=False, sort='100', state=False))
        self.create_data(ProdInfo(name='重复卡密演示', prod_cag_name="激活码", prod_info='商品简述信息演示XXXX', prod_img_url="images/null.png", prod_discription="示例：卡密格式：账号------密码-----", prod_price=9.99, prod_price_wholesale=None, prod_sales=0, prod_tag="限时优惠", auto=True, sort='100', state=True))
        self.create_data(ProdInfo(name='普通商品CC', prod_cag_name="激活码", prod_info='商品简述信息演示XXXX', prod_img_url="images/null.png", prod_discription="示例：卡密格式：账号------密码-----", prod_price=9.99, prod_price_wholesale=None, prod_sales=0, prod_tag="限时优惠", auto=True, sort='100', state=True))
        self.create_data(ProdInfo(name='普通商品BB', prod_cag_name="激活码", prod_info='商品简述信息演示XXXX', prod_img_url="images/null.png", prod_discription="示例：卡密格式：账号------密码-----", prod_price=9.99, prod_price_wholesale=None, prod_sales=0, prod_tag="限时优惠", auto=True, sort='100', state=False))

        # 卡密设置
        self.create_data(Card(prod_name='普通商品演示', card='454545454454545454', reuse=False, isused=False))
        self.create_data(Card(prod_name='批发商品演示', card='555555555555555555', reuse=False, isused=False))
        self.create_data(Card(prod_name='批发商品演示', card='666666666666666666', reuse=False, isused=False))
        self.create_data(Card(prod_name='重复卡密演示', card='666666666666666666', reuse=True, isused=False))

        # 系统配置
        self.create_data(Config(name='icp', info='<a style="color: #fafafa;" href="https://www.baidu.com">川ICP备1101XXXX号-10</a>', description='可填写备案信息', isshow=True))
        self.create_data(Config(name='home_notice', info='稳定版演示站点，公告信息可在后台设置', description='首页公告', isshow=True))
        self.create_data(Config(name='other_optional', info='{"login_mode": 1, "tourist_orders": 1, "front_desk_inventory_display": 1, "front_end_sales_display": 1, "sales_statistics": 1}', description='[1左边按钮，0右边按钮] 强制登录|允许游客下单; 开|关; 文字【少量、缺货或充足】 数字0-9999 ; 是|否 ; 自动统计|仅限手工修改', isshow=True))

        self.create_data(Config(name='web_name', info='KAMIFAKA', description='网站名称', isshow=True))
        self.create_data(Config(name='web_keyword', info='关键词、收录词汇', description='网站关键词', isshow=True))
        self.create_data(Config(name='description', info='网站描述信息。。。', description='网站描述', isshow=True))
        self.create_data(Config(name='web_url', info='http://localhost:80', description='必填，网站实际地址', isshow=True))
        self.create_data(Config(name='web_bg_url', info='https://cdn.jsdelivr.net/gh/Baiyuetribe/yyycode@dev/colorfull.jpg', description='网站背景图片', isshow=True))
        self.create_data(Config(name='contact_us', info='<p>示例，请在管理后台>>网站设置里修改，支持HTML格式</p>', description='首页-联系我们', isshow=True))
        self.create_data(Config(name='toast_notice', info='稳定版演示站点，公告信息可在后台设置', description='首页滑动消息设置', isshow=True))
        # self.create_data(Config(name='modal_notice', info='【计划中】','全局弹窗信息', isshow=True))
        self.create_data(Config(name='contact_option', info='0', description='是否启用联系方式查询[0启用，1关闭]', isshow=True))
        self.create_data(Config(name='theme', info='list', description='主题', isshow=False))
        self.create_data(Config(name='store_url', info='https://www.baidu.com', description='Github项目地址，用于手动检测新版', isshow=False))
        self.create_data(Config(name='store_v', info='0.1.0', description='Github项目地址，用于手动检测新版', isshow=False))

        # 通知渠道 ：名称；对管理员开关；对用户开关；对管理员需要管理员账号；用户无；名称+config+管理员+admin_switch+user_switch
        self.create_data(Notice(name='邮箱通知', config="{'sendname':'no_replay','sendmail':'demo@gmail.com','smtp_address':'smtp.163.com','smtp_port':'465','smtp_pwd':'ZZZZZZZ'}", admin_account='demo@qq.com', admin_switch=False, user_switch=False))
        self.create_data(Notice(name='微信通知', config="{'token':'AT_nvlYDjev89gV96hBAvUX5HR3idWQwLlA'}", admin_account='xxxxxxxxxxxxxxxx', admin_switch=False, user_switch=False))
        self.create_data(Notice(name='TG通知', config="{'TG_TOKEN':'1290570937:AAHaXA2uOvDoGKbGeY4xVIi5kR7K55saXhs'}", admin_account='445545444', admin_switch=False, user_switch=False))
        self.create_data(Notice(name='短信通知', config="{'username':'XXXXXX','password':'YYYYY','tokenYZM':'必填','templateid':'必填'}", admin_account='15347875415', admin_switch=False, user_switch=False))
        self.create_data(Notice(name='QQ通知', config="{'Key':'null'}", admin_account='格式：您的KEY@已添加的QQ号,示例：abc@123', admin_switch=False, user_switch=False))

        # 订单信息【测试环境】
        self.create_data(Order(out_order_id='演示订单可删除', name='普通商品演示', payment='支付宝当面付', contact='472835979', contact_txt='请求尽快发货', price=9.99, num=1, total_price=0.9, card='账号：xxxxx；密码：xxxx', status=None))
        self.create_data(Order(out_order_id='演示订单可删除2', name='普通商品演示', payment='虎皮椒微信', contact='458721@qq.com', contact_txt='非常感谢', price=9.99, num=3, total_price=1.97, card=None, status=None))  # 卡密为None或‘’空都可以
        self.create_data(Order(out_order_id='Order_1608107857954q7kyldyg', name='普通商品演示', payment='虎皮椒支付宝', contact='demo@gmail.com', contact_txt='不错', price=9.99, num=1, total_price=0.9, card='此处为卡密', status=None))
        self.create_data(Order(out_order_id='演示订单4457', name='普通商品演示', payment='虎皮椒支付宝', contact='472835979', contact_txt='不错', price=9.99, num=1, total_price=1.9, card='TG卡密DEMO', status=None))

        # 插件配置信息
        self.create_data(Plugin(name='TG发卡', config="{'TG_TOKEN':'1488086653:AAHihuO0JuvmiDNZtsYcDBpUhL1rTDO6o1C'}", about='### 示例 \n请在管理后台--》Telegram里设置，支持HTML格式', switch=False))
        self.create_data(Plugin(name='微信公众号', config="{'PID':'xxxxxxxxxxxx'}", about='<p>示例，请在管理后台>>Telegram里设置，支持HTML格式</p>', switch=False))

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

    def create_data(self, record):
        """添加记录"""
        with self.session_scope() as session:
            session.add(record)

    def read_data(self, model, uid: int):
        """获取单条记录"""
        with self.session_scope() as session:
            return session.query(model).filter(model.id == uid).first()

    def read_datas(self, input_model, output_model, skip=0, limit=10):
        """获取所有记录"""
        with self.session_scope() as session:
            # 获取总记录数
            total_elements = session.execute(select(func.count(input_model.id))).scalar()
            # 获取记录
            result = session.execute(select(input_model).offset(skip).limit(limit))
            infos = result.scalars().all()
            # 计算总页数
            total_pages = (total_elements + limit - 1) // limit
            current_page = (skip // limit) + 1
            data = [output_model.from_orm(info) for info in infos]
            return {"records": data, "pager": {"page": current_page, "pageSize": total_pages, "total": total_elements}}

    def update_data(self, model, dic):
        """更新记录"""
        with self.session_scope() as session:
            record = session.query(model).filter_by(id=dic["id"]).first()
            if record:
                for key, value in dic.items():
                    setattr(record, key, value)
                session.add(record)
                return record
            return None

    def update_data_name(self, model, dic):
        """更新记录"""
        with self.session_scope() as session:
            record = session.query(model).filter_by(name=dic["name"]).first()
            if record:
                for key, value in dic.items():
                    setattr(record, key, value)
                session.add(record)
                return record
            return None

    def delete_data(self, model, uid):
        """删除记录"""
        with self.session_scope() as session:
            record = session.query(model).filter_by(id=uid).first()
            session.delete(record)
            return record

    def create_batch_data(self, records: List[T]):
        """批量添加记录"""
        with self.session_scope() as session:
            session.add_all(records)

    def delete_batch_data(self, model, filter_params):
        """批量删除记录"""
        with self.session_scope() as session:
            records = session.query(model).filter_by(**filter_params).all()
            for record in records:
                session.delete(record)
            return records

    def delete_card_duplicates(self):
        """定制: 删除重复的卡片"""
        with self.session_scope() as session:
            distinct_cards = session.execute(select(Card).distinct(Card.card)).scalars().all()  # 查询所有卡片，按 card 列去重
            distinct_card_ids = {card.id for card in distinct_cards}  # 获取所有卡片的 ID
            session.query(Card).filter(Card.id.notin_(distinct_card_ids)).delete(synchronize_session='fetch')  # 删除重复的卡片

    def search_dashboard(self):
        """获取所有记录"""
        with self.session_scope() as session:
            # 获取当前时间
            now = datetime.now()
            # 今日开始时间
            today = now.date()
            # 昨日时间段
            yesterday_start = today - timedelta(days=1)
            yesterday_end = today
            # 本月开始时间
            start_of_month = datetime(now.year, now.month, 1)
            # 上月时间段
            start_of_last_month = (start_of_month - timedelta(days=1)).replace(day=1)
            end_of_last_month = start_of_month - timedelta(days=1)

            # 成交订单数
            total_orders = session.query(func.count(Order.id)).filter(Order.status == True).scalar()
            # 总收益
            total_revenue = session.query(func.sum(Order.total_price)).scalar()
            # 总用户
            total_users = session.query(func.count(User.id)).scalar()
            # 剩余库存
            total_stock = session.query(func.count(Card.id)).scalar()

            """订单统计 天 周 月 年 | 总计"""
            def get_hourly_intervals(last_24_hours):
                intervals = []
                for i in range(24):
                    hour = last_24_hours + timedelta(hours=i)
                    intervals.append(hour.strftime('%Y-%m-%d %H:00:00'))
                return intervals

            def get_daily_intervals(last_n_days, n):
                intervals = []
                for i in range(n):
                    day = last_n_days + timedelta(days=i)
                    intervals.append(day.strftime('%Y-%m-%d'))
                return intervals

            def get_monthly_intervals(last_12_months):
                intervals = []
                for i in range(12):
                    month = last_12_months + timedelta(days=30 * i)  # 粗略的近似
                    intervals.append(month.strftime('%Y-%m'))
                return intervals

            # 前24小时，每小时的销售金额总和
            last_24_hours = now - timedelta(hours=24)
            hourly_sum = session.query(
                func.strftime('%Y-%m-%d %H:00:00', Order.updatetime).label('hour'),
                func.sum(Order.total_price).label('sum_price')
            ).filter(Order.updatetime >= last_24_hours).group_by('hour').all()
            hourly_sum_dict = {hour: sum_price for hour, sum_price in hourly_sum}
            all_hours = get_hourly_intervals(last_24_hours)
            hourly_sum_dict = {hour: hourly_sum_dict.get(hour, 0) for hour in all_hours}

            # 前7天，每天的销售金额总和
            last_7_days = now - timedelta(days=7)
            daily_sum_last_7_days = session.query(
                func.strftime('%Y-%m-%d', Order.updatetime).label('day'),
                func.sum(Order.total_price).label('sum_price')
            ).filter(Order.updatetime >= last_7_days).group_by('day').all()
            daily_sum_last_7_days_dict = {day: sum_price for day, sum_price in daily_sum_last_7_days}
            all_days_last_7_days = get_daily_intervals(last_7_days, 7)
            daily_sum_last_7_days_dict = {day: daily_sum_last_7_days_dict.get(day, 0) for day in all_days_last_7_days}

            # 前30天，每天的销售金额总和
            last_30_days = now - timedelta(days=30)
            daily_sum_last_30_days = session.query(
                func.strftime('%Y-%m-%d', Order.updatetime).label('day'),
                func.sum(Order.total_price).label('sum_price')
            ).filter(Order.updatetime >= last_30_days).group_by('day').all()
            daily_sum_last_30_days_dict = {day: sum_price for day, sum_price in daily_sum_last_30_days}
            all_days_last_30_days = get_daily_intervals(last_30_days, 30)
            daily_sum_last_30_days_dict = {day: daily_sum_last_30_days_dict.get(day, 0) for day in all_days_last_30_days}

            # 前12个月，每月的销售金额总和
            last_12_months = now - timedelta(days=365)  # 粗略的近似
            monthly_sum = session.query(
                func.strftime('%Y-%m', Order.updatetime).label('month'),
                func.sum(Order.total_price).label('sum_price')
            ).filter(Order.updatetime >= last_12_months).group_by('month').all()
            monthly_sum_dict = {month: sum_price for month, sum_price in monthly_sum}
            all_months = get_monthly_intervals(last_12_months)
            monthly_sum_dict = {month: monthly_sum_dict.get(month, 0) for month in all_months}

            order_statistics = {"day": hourly_sum_dict,
                                "day_money": sum(hourly_sum_dict.values()),
                                "week": daily_sum_last_7_days_dict,
                                "week_money": sum(daily_sum_last_7_days_dict.values()),
                                "month": daily_sum_last_30_days_dict,
                                "month_money": sum(daily_sum_last_30_days_dict.values()),
                                "year": monthly_sum_dict,
                                "year_money": sum(monthly_sum_dict.values())}

            # 热销榜单 前五销量名称 及 销售数量
            top_5_products = session.query(Order.name,
                                           func.count(Order.id).label('sales_count')).filter(Order.status == True
                                          ).group_by(Order.name).order_by(desc('sales_count')).limit(5).all()
            top_5_products = {product: count for product, count in top_5_products}

            # 今日订单数
            today_orders = session.query(func.count(Order.id)).filter(Order.status==True, Order.updatetime.between(today, now)).scalar()
            # 今日收益
            today_revenue = session.query(func.sum(Order.total_price)).filter(Order.status==True, Order.updatetime.between(today, now)).scalar()
            # 本月订单数
            month_orders = session.query(func.count(Order.id)).filter(Order.status==True, Order.updatetime.between(start_of_month, now)).scalar()
            # 本月收益
            month_revenue = session.query(func.sum(Order.total_price)).filter(Order.status==True, Order.updatetime.between(start_of_month, now)).scalar()
            # 昨日订单数
            yesterday_orders = session.query(func.count(Order.id)).filter(Order.status==True, Order.updatetime.between(yesterday_start, yesterday_end)).scalar()
            # 昨日收益
            yesterday_revenue = session.query(func.sum(Order.total_price)).filter(Order.status==True, Order.updatetime.between(yesterday_start, yesterday_end)).scalar()
            # 上月订单数
            last_month_orders = session.query(func.count(Order.id)).filter(Order.status==True, Order.updatetime.between(start_of_last_month, end_of_last_month)).scalar()
            # 上月收益
            last_month_revenue = session.query(func.sum(Order.total_price)).filter(Order.status==True, Order.updatetime.between(start_of_last_month, end_of_last_month)).scalar()
            return {"total_orders": total_orders, "total_revenue": total_revenue, "total_users": total_users, "total_stock": total_stock,
                    "order_statistics": order_statistics,
                    "today_orders": today_orders, "today_revenue": today_revenue, "month_orders": month_orders, "month_revenue": month_revenue,
                    "yesterday_orders": yesterday_orders, "yesterday_revenue": yesterday_revenue, "last_month_orders": last_month_orders, "last_month_revenue": last_month_revenue,
                    "top_5_products": top_5_products}

    def search_data(self, model, output_model, filter_params):
        """查询记录"""
        with self.session_scope() as session:
            record = session.query(model).filter(*filter_params).first()
            return output_model.from_orm(record)

    def search_filter(self, model, output_model, filter_params):
        """查询记录"""
        with self.session_scope() as session:
            records = session.query(model).filter(*filter_params).all()
            return [output_model.from_orm(record) for record in records]

    def search_filter_page_turning(self, model, output_model, filter_params, page: int, page_size: int):
        """查询记录"""
        with self.session_scope() as session:
            query = session.query(model).filter(*filter_params)
            total_elements = query.count()
            records = query.offset((page - 1) * page_size).limit(page_size).all()
            # 计算总页数和当前页
            total_pages = (total_elements + page_size - 1) // page_size
            current_page = page
            data = [output_model.from_orm(record) for record in records]
            return {"records": data, "pager": {"page": current_page, "pageSize": total_pages, "total": total_elements}}

    def get_all_records(self, model):
        """获取所有记录"""
        with self.session_scope() as session:
            return session.query(model).all()


# 示例用法
if __name__ == "__main__":
    Database().create_tables()  # 使用 SQLite 数据库
    Database().create_example_data()  # 创建数据样本

    # # 测试插入示例数据
    # db.create_data(AdminUser(email="admin@qq.com", hash="admin"))
    # # 测试查询示例数据
    # with db.session_scope() as session:
    #     user = session.query(AdminUser).filter_by(id=1).first()
    #     print(f"Retrieved User: {AdminUser.email}, {AdminUser.hash}")
    # # 测试更新示例数据
    # db.update_record(AdminUser, 1, email="admin", hash="123")

    # # 测试删除示例数据
    # db.delete_record(User, 1)
    # # 测试清空示例数据
    # db.clear_table(User)
    # # 测试删除数据库
    # db.drop_tables()
