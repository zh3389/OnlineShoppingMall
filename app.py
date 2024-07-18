import os
import ast
import shutil
from pathlib import Path
import datetime
import random
import string
import asyncio
import uvicorn
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request, Response, Depends, Form, File, UploadFile, Query
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
from utils.usersManager import User, UserCreate, UserRead, UserUpdate, auth_backend, fastapi_users, init_user_tabel
from utils.usersManager import current_user, current_active_user, current_active_verified_user, current_superuser
from fastapi.middleware.cors import CORSMiddleware
from utils.databaseManager import Database
from sqlalchemy import or_


app = FastAPI()


"""
数据库初始化
"""
def init_database():
    from sqlalchemy import create_engine, inspect
    databaseURL = 'sqlite:///./utils/database.db'
    engine = create_engine(databaseURL)  # 创建数据库引擎
    inspector = inspect(engine)  # 使用inspect来检查数据库中的表
    table_names = inspector.get_table_names()  # 获取所有表名
    print("数据库表名:", table_names)
    # 判断表是否存在
    if 'order' not in table_names:
        Database(databaseURL).create_tables()
        Database(databaseURL).create_example_data()
    if 'user' not in table_names:
        asyncio.run(init_user_tabel())
    db = Database(databaseURL)
    return db


db = init_database()


# 配置 CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
)


# 仪表盘
@app.get("/api/backend/dashboard", tags=["TodoBackend"])
async def get_dashboard():
    """
    获取仪表盘数据
    """
    result = db.search_dashboard()
    return result


"""
========================================
分类管理
========================================
"""
from utils.databaseManager import ProdCag
from utils.databaseSchemas import ProdCagID, ProdCagCreate, ProdCagUpdate, ProdCagResponse


@app.get("/api/backend/class_read/{skip}/{limit}", tags=["backend"])
async def classification_read(skip: int = 0, limit: int = 10):
    """
    获取分类列表
    """
    prodcags = db.read_data(ProdCag, ProdCagResponse, skip, limit)
    return {"code": 200,
            "data": {"data": prodcags},
            "msg": "分类查询成功"
            }


@app.post("/api/backend/class_create", tags=["backend"])
async def classification_create(cla: ProdCagCreate):
    """
    新增分类
    """
    data_dict = dict(cla)
    data = ProdCag(**data_dict)
    db.create_data(data)
    return {"code": 200,
            "data": data_dict,
            "msg": "分类新增成功"
            }


@app.patch("/api/backend/class_update", tags=["backend"])
async def classification_update(cla: ProdCagUpdate):
    """
    修改分类
    """
    data = dict(cla)
    db.update_data(ProdCag, data)
    return {"code": 200,
            "data": data,
            "msg": "分类修改成功"
            }


@app.delete("/api/backend/class_delete", tags=["backend"])
async def classification_delete(cla: ProdCagID):
    """
    删除分类
    """
    db.delete_data(ProdCag, cla.id)
    return {"code": 200,
            "data": {"id": cla.id},
            "msg": "分类删除成功"
            }

"""
========================================
商品管理
========================================
"""
from utils.databaseManager import ProdInfo
from utils.databaseSchemas import ProdInfoID, ProdInfoCreate, ProdInfoUpdate, ProdInfoResponse


@app.get("/api/backend/product_read/{skip}/{limit}", tags=["backend"])
async def product_read(skip: int = 0, limit: int = 10):
    """
    获取商品列表
    """
    prodinfos = db.read_data(ProdInfo, ProdInfoResponse, skip, limit)
    return {"code": 200,
            "data": {"data": prodinfos},
            "msg": "商品信息查询成功"
            }


@app.post("/api/backend/product_create", tags=["backend"])
async def product_create(cla: ProdInfoCreate):
    """
    新增商品
    """
    data_dict = dict(cla)
    data = ProdInfo(**data_dict)
    db.create_data(data)
    return {"code": 200,
            "data": data_dict,
            "msg": "商品信息新增成功"
            }


@app.patch("/api/backend/product_update", tags=["backend"])
async def product_update(cla: ProdInfoUpdate):
    """
    修改商品
    """
    data = dict(cla)
    db.update_data(ProdInfo, data)
    return {"code": 200,
            "data": data,
            "msg": "商品信息修改成功"
            }


@app.delete("/api/backend/product_delete", tags=["backend"])
async def product_delete(cla: ProdInfoID):
    """
    删除商品
    """
    db.delete_data(ProdInfo, cla.id)
    return {"code": 200,
            "data": {"id": cla.id},
            "msg": "商品信息删除成功"
            }


"""
========================================
卡密管理
========================================
"""
from utils.databaseManager import Card
from utils.databaseSchemas import CardID, CardCreate, CardUpdate, CardResponse, CardFilterDelete


@app.get("/api/backend/cami_read/{skip}/{limit}", tags=["backend"])
async def cami_read(skip: int = 0, limit: int = 10):
    """
    获取卡密列表
    """
    camis = db.read_data(Card, CardResponse, skip, limit)
    return {"code": 200,
            "data": {"data": camis},
            "msg": "卡密查询成功"
            }


@app.post("/api/backend/cami_create", tags=["backend"])
async def cami_create(cla: CardCreate):
    """
    新增卡密
    """
    lines = cla.card.splitlines()
    data_list = [Card(prod_name=cla.prod_name, card=line, reuse=cla.reuse) for line in lines]
    db.create_batch_data(data_list)
    return {"code": 200,
            "data": "数据太多暂不展示",
            "msg": "卡密新增成功"
            }


@app.patch("/api/backend/cami_update", tags=["backend"])
async def cami_update(cla: CardUpdate):
    """
    修改卡密
    """
    data = dict(cla)
    db.update_data(Card, data)
    return {"code": 200,
            "data": data,
            "msg": "卡密修改成功"
            }


@app.get("/api/backend/cami_search/{cardstr}/{skip}/{limit}", tags=["backend"])
async def cami_search(cardstr: str, skip: int, limit: int):
    """
    搜索卡密
    """
    camis = db.search_filter_page_turning(Card, CardResponse, {Card.card.like(f"%{cardstr}%")}, skip, limit)
    return {"code": 200,
            "data": camis,
            "msg": "卡密搜索成功"
            }


@app.delete("/api/backend/cami_batch_delete", tags=["backend"])
async def cami_batch_delete(cla: CardFilterDelete):
    """
    批量删除卡密
    """
    dic = {}
    for key, value in dict(cla).items():
        if value is not None:
            dic[key] = value
    print("=" * 100)
    print(dic)
    db.delete_batch_data(Card, dic)
    return {"message": "卡密删除成功"}


@app.delete("/api/backend/cami_clear_duplicates", tags=["backend"])
async def cami_clear_duplicates():
    """
    一键卡密去重
    """
    db.delete_card_duplicates()
    return {"code": 200,
            "data": "无需展示数据",
            "msg": "重复卡密清理成功"
            }


@app.delete("/api/backend/cami_delete", tags=["backend"])
async def cami_delete(cla: CardID):
    """
    删除卡密
    """
    db.delete_data(Card, cla.id)
    return {"code": 200,
            "data": {"id": cla.id},
            "msg": "卡密删除成功"
            }


"""
========================================
优惠券管理
========================================
"""


@app.get("/api/backend/coupon_read", tags=["TodoBackend"])
async def coupon_read():
    """
    获取优惠券列表
    """
    return {"message": "优惠券列表"}


@app.post("/api/backend/coupon_create", tags=["TodoBackend"])
async def coupon_create():
    """
    新增优惠券
    """
    return {"message": "优惠券新增成功"}


@app.patch("/api/backend/coupon_update", tags=["TodoBackend"])
async def coupon_update():
    """
    修改优惠券
    """
    return {"message": "优惠券修改成功"}


@app.delete("/api/backend/coupon_delete", tags=["TodoBackend"])
async def coupon_delete():
    """
    删除优惠券
    """
    return {"message": "优惠券删除成功"}


@app.patch("/api/backend/coupon_switch", tags=["TodoBackend"])
async def coupon_switch():
    """
    开关优惠券
    """
    return {"message": "优惠券开关成功"}


"""
========================================
订单管理
========================================
"""
from utils.databaseManager import Order
from utils.databaseSchemas import OrderBase, OrderResponse, OrderDelete, OrderSearch


@app.get("/api/backend/order_read/{skip}/{limit}", tags=["backend"])
async def order_read(skip: int = 0, limit: int = 10):
    """
    获取订单列表
    """
    orders = db.read_data(Order, OrderResponse, skip, limit)
    return {"code": 200,
            "data": {"data": orders},
            "msg": "订单查询成功"
            }


@app.post("/api/backend/order_search", tags=["backend"])
async def order_search(cla: OrderSearch, skip: int = 0, limit: int = 10):
    """
    搜索订单
    """
    filter_params = [or_(Order.out_order_id.like(f"%{cla.out_order_id}%"), Order.contact.like(f"%{cla.contact}%"), Order.card.like(f"%{cla.card}%"))]
    orders = db.search_filter_page_turning(Order, OrderResponse, filter_params, skip, limit)
    return {"code": 200,
            "data": {"data": orders},
            "msg": "订单查询成功"
            }


@app.delete("/api/backend/order_delete", tags=["backend"])
async def order_delete(cla: OrderDelete):
    """
    删除订单
    """
    db.delete_data(Order, cla.id)
    return {"code": 200,
            "data": {"id": cla.id},
            "msg": "订单删除成功"
            }


@app.delete("/api/backend/order_delete_all", tags=["backend"])
async def order_delete_all():
    """
    删除订单
    """
    db.delete_batch_data(Order, {"status": 0})
    return {"code": 200,
            "data": {},
            "msg": "所有未完成订单删除成功"
            }


"""
========================================
用户管理
========================================
"""
from utils.usersManager import User, UserID, UserResponse, UserUpdate


@app.get("/api/backend/user_read/{skip}/{limit}", tags=["backend"])
async def user_read(skip: int = 0, limit: int = 10):
    """
    获取用户列表
    """
    users = db.read_data(User, UserResponse, skip, limit)
    return {"code": 200,
            "data": {"data": users},
            "msg": "用户查询成功"
            }


@app.get("/api/backend/user_search/{skip}/{limit}", tags=["backend"])
async def user_search(userstr: str, skip: int = 0, limit: int = 10):
    """
    搜索用户
    """
    filter_params = [or_(User.email.like(f"%{userstr}%"))]
    users = db.search_filter_page_turning(User, UserResponse, filter_params, skip, limit)
    return {"code": 200,
            "data": {"data": users},
            "msg": "搜索用户成功"
            }


@app.patch("/api/backend/user_reset", tags=["backend"])
async def user_reset(cla: UserID):
    """
    重置用户密码
    """
    return {"code": 200,
            "data": {"data": cla.id},
            "msg": "用户密码重置成功(暂未实现)"
            }


@app.delete("/api/backend/user_delete", tags=["backend"])
async def user_delete(cla: UserID):
    """
    删除用户
    """
    db.delete_data(User, cla.id)
    return {"code": 200,
            "data": {"id": cla.id},
            "msg": "用户删除成功"
            }


"""
========================================
图床管理
========================================
"""


UPLOAD_DIR = "drawingbed"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def generate_random_filename(extension: str) -> str:
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=6))
    return f"{timestamp}_{random_str}.{extension}"


@app.get("/api/backend/drawingbed_read/", tags=["backend"])
async def drawingbed_read(skip: int = 0, limit: int = 10):
    files = list(Path(UPLOAD_DIR).iterdir())
    total_files = len(files)
    start = skip * limit
    end = start + limit
    files_on_page = files[start:end]
    file_names = [file.name for file in files_on_page]
    data = []
    for file_name in file_names:
        file_location = Path(UPLOAD_DIR) / file_name
        data.append({"filename": file_name, "file_location": file_location})
    return {"code": 200,
            "data": {"data": data, "pager": {"page": skip, "pageSize": limit, "total": total_files}},
            "msg": "图像查询成功"
            }


@app.get("/api/backend/drawingbed_show/{filename}", tags=["backend"])
async def drawingbed_show(filename: str):
    file_location = Path(UPLOAD_DIR) / filename
    if file_location.exists():
        return FileResponse(file_location)
    else:
        return {"code": 404,
                "data": {"file_location": file_location},
                "msg": "找不到文件"
                }


@app.post("/api/backend/drawingbed_create", tags=["backend"])
async def drawingbed_create(file: UploadFile = File(...)):
    """
    新增图床
    """
    extension = file.filename.split(".")[-1]
    filename = generate_random_filename(extension)
    file_location = Path(UPLOAD_DIR) / filename
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"code": 200,
            "data": {"filename": filename, "file_location": file_location},
            "msg": "图像上传成功"
            }


@app.delete("/api/backend/drawingbed_delete/{filename}", tags=["backend"])
async def drawingbed_delete(filename: str):
    """
    删除图床
    """
    file_location = Path(UPLOAD_DIR) / filename
    if file_location.exists():
        os.remove(file_location)
        return {"code": 200,
                "data": {"file_location": file_location},
                "msg": "图像删除成功"
                }
    else:
        return {"code": 404,
                "data": {"file_location": file_location},
                "msg": "找不到文件"
                }


"""
========================================
佣金记录
========================================
"""


@app.get("/api/backend/invite", tags=["TodoBackend"])
async def get_invite():
    """
    获取佣金记录列表
    """
    return {"message": "佣金记录列表"}


@app.get("/api/backend/invite_search", tags=["TodoBackend"])
async def search_invite(keyword: str, ):
    """
    搜索佣金记录
    """
    return {"message": "搜索佣金记录"}


@app.delete("/api/backend/invite_delete", tags=["TodoBackend"])
async def delete_invite(invite_id: int, ):
    """
    删除佣金记录
    """
    return {"message": "佣金记录删除成功"}


"""
========================================
主题设置
========================================
"""


@app.get("/api/backend/theme", tags=["TodoBackend"])
async def get_theme():
    """
    获取主题设置
    """
    return {"message": "主题设置"}


class Theme(BaseModel):
    name: str
    description: Optional[str] = None


@app.patch("/api/backend/theme_update", tags=["TodoBackend"])
async def update_theme(theme: Theme, ):
    """
    更新主题设置
    """
    return {"message": "主题设置更新成功"}


"""
========================================
支付接口设置
========================================
"""


@app.get("/api/backend/payment", tags=["TodoBackend"])
async def get_payment():
    """
    获取支付接口设置
    """
    return {"message": "支付接口设置"}


@app.patch("/api/backend/payment_update", tags=["TodoBackend"])
async def update_payment(payment: dict, ):
    """
    更新支付接口设置
    """
    return {"message": "支付接口设置更新成功"}


"""
========================================
消息通知
========================================
"""
from utils.databaseManager import Notice
from utils.databaseSchemas import NoticeResponse
from utils.utils import EmailManager


@app.get("/api/backend/message", tags=["TodoBackend"])
async def get_message():
    """
    获取消息通知设置
    """
    return {"message": "消息通知设置"}


@app.post("/api/backend/send_email_test", tags=["backend"])
async def send_email(addressee: str = 'admin@qq.com', subject: str = '测试邮件', content: str = '今日报告已生成，请查收。'):
    """
    测试SMTP
    """
    email_param = db.search_data(Notice, NoticeResponse, [Notice.name == '邮箱通知'])
    email_param = ast.literal_eval(email_param.config)
    emailM = EmailManager(smtp_address=email_param['smtp_address'], sendmail=email_param['sendmail'], send_name=email_param['sendmail'], smtp_pwd=email_param['smtp_pwd'], smtp_port=email_param['smtp_port'])
    emailM.send_email(addressee, subject, content)
    return {"code": 200,
            "data": email_param,
            "msg": "SMTP测试成功"
            }


@app.patch("/api/backend/save_email_settings", tags=["backend"])
async def save_email_settings(config: dict ={'sendname':'no_replay','sendmail':'demo@gmail.com','smtp_address':'smtp.163.com','smtp_port':'465','smtp_pwd':'ZZZZZZZ'}):
    """
    保存SMTP设置
    """
    try:
        dic = {}
        dic["name"] = "邮箱通知"
        dic["config"] = str(config)
        dic["admin_account"] = "admin@qq.com"
        db.update_data_name(Notice, dic)
    except Exception as e:
        db.create_data(Notice(name="邮箱通知", config=str(config), admin_account="admin@qq.com"))
    return {"code": 200,
            "data": config,
            "msg": "SMTP设置保存成功"
            }


@app.post("/api/backend/message_admin_test", tags=["TodoBackend"])
async def send_admin_message():
    """
    测试Admin消息
    """
    return {"message": "Admin消息测试成功"}


@app.patch("/api/backend/message_admin_set", tags=["TodoBackend"])
async def set_admin_message(settings: dict, ):
    """
    设置Admin消息
    """
    return {"message": "Admin消息设置成功"}


@app.patch("/api/backend/message_switch", tags=["TodoBackend"])
async def switch_message(status: bool, ):
    """
    切换消息开关
    """
    return {"message": "消息开关切换成功"}


"""
========================================
综合设置
========================================
"""
from utils.databaseManager import Config
from utils.databaseSchemas import ConfigResponse


@app.get("/api/backend/get_other_config", tags=["backend"])
async def get_other_config():
    """
    获取综合设置
    """
    result = db.search_filter(Config, ConfigResponse, {})
    return {"code": 200,
            "data": result,
            "msg": "综合设置查询成功"
            }


@app.patch("/api/backend/home_notice", tags=["backend"])
async def update_home_notice(home_notice: str):
    """
    更新店铺公告
    """
    dic = {"name": "home_notice", "info": home_notice, "description": "首页公告", "isshow": True}
    db.update_data_name(Config, dic)
    return {"code": 200,
            "data": dic,
            "msg": "店铺公告更新成功"
            }


@app.patch("/api/backend/icp", tags=["backend"])
async def update_icp(icp: str):
    """
    更新底部备案
    """
    dic = {"name": "icp", "info": icp, "description": "底部备案", "isshow": True}
    db.update_data_name(Config, dic)
    return {"code": 200,
            "data": dic,
            "msg": "底部备案更新成功"
            }


@app.patch("/api/backend/other_optional", tags=["backend"])
async def update_other_optional(other_optional: dict={"login_mode": 1, "tourist_orders": 1, "front_desk_inventory_display": 1, "front_end_sales_display": 1, "sales_statistics": 1}):
    """
    更新可选参数
    """
    dic = {"name": "other_optional", "info": str(other_optional), "description": "可选参数", "isshow": True}
    db.update_data_name(Config, dic)
    return {"code": 200,
            "data": dic,
            "msg": "可选参数更新成功"
            }


@app.patch("/api/backend/admin_reset", tags=["TodoBackend"])
async def reset_admin_account(cla: dict):
    """
    管理员账密修改
    """
    return {"code": 200,
            "data": "暂未实现",
            "msg": "管理员账密修改成功"
            }


"""
========================================
返回商店主页
========================================
"""


@app.get("/api/backend/home", tags=["TodoBackend"])
async def return_home():
    """
    返回商店主页
    """
    return {"message": "返回商店主页"}


"""
========================================
退出登录
========================================
"""


@app.get("/api/backend/logout", tags=["TodoBackend"])
async def logout():
    """
    退出登录，清除COOKIE
    """
    return {"message": "退出登录成功"}


@app.get("/api/frontend/user_invitation", tags=["TodoFrontend"])
async def user_invitation(user: User = Depends(current_active_verified_user)):
    """
    获取邀请好友信息接口
    """
    return {"message": "邀请好友"}


@app.get("/api/frontend/user_center", tags=["TodoFrontend"])
async def user_center(user: User = Depends(current_active_user)):
    """
    获取个人中心信息接口
    """
    return {"message": "个人中心"}


@app.get("/api/frontend/user_wallet", tags=["TodoFrontend"])
async def user_wallet(user: User = Depends(current_active_user)):
    """
    获取我的钱包信息接口
    """
    return {"message": "我的钱包"}


@app.get("/api/frontend/user_order", tags=["TodoFrontend"])
async def user_order(user: User = Depends(current_active_user)):
    """
    获取订单中心信息接口
    """
    return {"message": "订单中心"}


@app.get("/api/frontend/user_order_query", tags=["TodoFrontend"])
async def user_order_query(order_id: Optional[int] = None, user: User = Depends(current_active_verified_user)):
    """
    查询订单信息接口
    """
    if order_id is not None and order_id in orders_db:
        return orders_db[order_id]
    return {"message": "订单查询"}


@app.get("/api/frontend/logout", tags=["TodoFrontend"])
async def logout(response: Response, user: User = Depends(current_active_user)):
    """
    用户退出登录接口，清除COOKIE
    """
    response.delete_cookie(key="session")
    return {"message": "退出登录成功"}


"""
返回给定身份验证后端的身份验证路由器。
：param backend:身份验证后端实例。
是否需要验证用户。默认为False。
"""
app.include_router(fastapi_users.get_auth_router(auth_backend),
                   prefix="/api/frontend",
                   tags=["auth"])

"""
返回一个带有注册路由的路由器。
：param UserRead：公共用户的Pydantic架构。
：param UserCreate：用于创建用户的Pydantic架构。
"""
app.include_router(fastapi_users.get_register_router(UserRead, UserCreate),
                   prefix="/api/frontend",
                   tags=["auth"],
                   )

"""
返回重置密码过程路由器。
"""
app.include_router(fastapi_users.get_reset_password_router(),
                   prefix="/api/frontend",
                   tags=["auth"],
                   )

"""
返回一个带有电子邮件验证路由的路由器。
：param UserRead：公共用户的Pydantic架构。
"""
app.include_router(fastapi_users.get_verify_router(UserRead),
                   prefix="/api/frontend",
                   tags=["auth"],
                   )

"""
返回一个带有路由的路由器来管理用户。
：param UserRead：公共用户的Pydantic架构。
：param UserUpdate：用于更新用户的Pydantic架构。
"""
app.include_router(fastapi_users.get_users_router(UserRead, UserUpdate),
                   prefix="/api/frontend",
                   tags=["users"],
                   )


@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    """
    一种处理对经过身份验证的路由的请求的函数。

    参数：
    - user: user，从当前活动的用户依赖关系中获取的用户对象。

    返回：
    - dict：包含用户电子邮件信息的词典。
    """
    return {"message": f"Hello {user.email}!"}


if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=8000)
