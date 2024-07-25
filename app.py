import os
import shutil
from pathlib import Path
import datetime
import random
import string
import uvicorn
from sqlalchemy import or_
from typing import Optional
from pydantic import BaseModel
from fastapi import FastAPI, Response, Depends, File, UploadFile, Query, responses
from fastapi.middleware.cors import CORSMiddleware
from utils import databaseSchemas as DbSchemas
from utils import usersManager as DbUsers
from utils import databaseManager as DbModels
from utils.databaseSchemas import ResponseModel
from utils.systemInit import SystemInit


app = FastAPI()
db = SystemInit().db
email_manager = SystemInit().create_email_manager()


# 配置 CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:8000",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


# 仪表盘
@app.get("/api/backend/dashboard", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def get_dashboard():
    """
    获取仪表盘数据
    """
    result = db.search_dashboard()
    return ResponseModel(code=200, data=result, msg="仪表盘数据获取成功")


"""
========================================
分类管理
========================================
"""


@app.get("/api/backend/class_read", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def classification_read(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    获取分类列表
    """
    prodcags = db.read_datas(DbModels.ProdCag, DbSchemas.ProdCagResponse, skip, limit)
    return ResponseModel(code=200, data=prodcags, msg="分类查询成功")


@app.post("/api/backend/class_create", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def classification_create(cla: DbSchemas.ProdCagCreate):
    """
    新增分类
    """
    data_dict = dict(cla)
    data = DbModels.ProdCag(**data_dict)
    if db.search_data(DbModels.ProdCag, DbSchemas.ProdCagResponse, [DbModels.ProdCag.name == cla.name]):
        return ResponseModel(code=500, data={}, msg="分类已存在")
    db.create_data(data)
    return ResponseModel(code=200, data=data_dict, msg="分类新增成功")


@app.patch("/api/backend/class_update", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def classification_update(cla: DbSchemas.ProdCagUpdate):
    """
    修改分类
    """
    data = dict(cla)
    record = db.update_data(DbModels.ProdCag, data)
    if record is None:
        return ResponseModel(code=500, data={}, msg="分类修改失败, 找不到指定的数据。")
    return ResponseModel(code=200, data=data, msg="分类修改成功")


@app.delete("/api/backend/class_delete", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def classification_delete(item_id: int):
    """
    删除分类
    """
    data = db.read_data(DbModels.ProdCag, item_id)
    if data is None:
        return ResponseModel(code=404, data={}, msg="找不到数据")
    record = db.delete_data(DbModels.ProdCag, item_id)
    if record is None:
        return ResponseModel(code=500, data={}, msg="分类删除失败")
    return ResponseModel(code=200, data={"id": item_id}, msg="分类删除成功")


"""
========================================
商品管理
========================================
"""


@app.get("/api/backend/product_read", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def product_read(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10), classify: Optional[str] = None):
    """
    获取商品列表
    """
    if classify is None:
        prodinfos = db.read_datas(DbModels.ProdInfo, DbSchemas.ProdInfoResponse, skip, limit)
    else:
        prodinfos = db.search_filter_page_turning(DbModels.ProdInfo, DbSchemas.ProdInfoResponse, {DbModels.ProdInfo.prod_cag_name == classify}, skip, limit)
    return ResponseModel(code=200, data=prodinfos, msg="商品信息查询成功")


@app.post("/api/backend/product_create", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def product_create(cla: DbSchemas.ProdInfoCreate):
    """
    新增商品
    """
    data_dict = dict(cla)
    data = DbModels.ProdInfo(**data_dict)
    if db.check_data(DbModels.ProdInfo, [DbModels.ProdInfo.name == cla.name]):
        return ResponseModel(code=500, data={}, msg="商品已存在")
    db.create_data(data)
    return ResponseModel(code=200, data=data_dict, msg="商品信息新增成功")


@app.patch("/api/backend/product_update", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def product_update(cla: DbSchemas.ProdInfoUpdate):
    """
    修改商品
    """
    data = dict(cla)
    record = db.update_data(DbModels.ProdInfo, data)
    if record is None:
        return ResponseModel(code=500, data={}, msg="商品信息修改失败, 找不到指定的数据。")
    return ResponseModel(code=200, data=data, msg="商品信息修改成功")


@app.delete("/api/backend/product_delete", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def product_delete(item_id: int):
    """
    删除商品
    """
    data = db.read_data(DbModels.ProdInfo, item_id)
    if data is None:
        return ResponseModel(code=404, data={}, msg="找不到数据")
    record = db.delete_data(DbModels.ProdInfo, item_id)
    if record is None:
        return ResponseModel(code=500, data={}, msg="商品信息删除失败, 找不到指定的数据。")
    return ResponseModel(code=200, data={"id": item_id}, msg="商品信息删除成功")


"""
========================================
卡密管理
========================================
"""


@app.get("/api/backend/cami_read", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def cami_read(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    获取卡密列表
    """
    camis = db.read_datas(DbModels.Card, DbSchemas.CardResponse, skip, limit)
    return ResponseModel(code=200, data=camis, msg="卡密查询成功")


@app.post("/api/backend/cami_create", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def cami_create(cla: DbSchemas.CardCreate):
    """
    新增卡密
    """
    lines = cla.card.splitlines()
    data_list = [DbModels.Card(prod_name=cla.prod_name, card=line, reuse=cla.reuse) for line in lines]
    db.create_batch_data(data_list)
    return ResponseModel(code=200, data={}, msg="卡密新增成功")


@app.patch("/api/backend/cami_update", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def cami_update(cla: DbSchemas.CardUpdate):
    """
    修改卡密
    """
    data = dict(cla)
    record = db.update_data(DbModels.Card, data)
    if record is None:
        return ResponseModel(code=500, data={}, msg="卡密修改失败, 找不到指定的数据。")
    return ResponseModel(code=200, data=data, msg="卡密修改成功")


@app.get("/api/backend/cami_search/{cardstr}", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def cami_search(cardstr: str, skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    搜索卡密
    """
    camis = db.search_filter_page_turning(DbModels.Card, DbSchemas.CardResponse, {DbModels.Card.card.like(f"%{cardstr}%")}, skip, limit)
    return ResponseModel(code=200, data=camis, msg="卡密搜索成功")


@app.delete("/api/backend/cami_batch_delete", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def cami_batch_delete(cla: DbSchemas.CardFilterDelete):
    """
    批量删除卡密
    """
    dic = {}
    for key, value in dict(cla).items():
        if value is not None:
            dic[key] = value
    print("=" * 100)
    print(dic)
    db.delete_batch_data(DbModels.Card, dic)
    return ResponseModel(code=200, data={}, msg="卡密批量删除成功")


@app.delete("/api/backend/cami_clear_duplicates", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def cami_clear_duplicates():
    """
    一键卡密去重
    """
    db.delete_card_duplicates()
    return ResponseModel(code=200, data={}, msg="卡密去重成功")


@app.delete("/api/backend/cami_delete", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def cami_delete(item_id: int):
    """
    删除卡密
    """
    data = db.read_data(DbModels.Card, item_id)
    if data is None:
        return ResponseModel(code=404, data={}, msg="找不到数据")
    record = db.delete_data(DbModels.Card, item_id)
    if record is None:
        return ResponseModel(code=500, data={}, msg="卡密删除失败, 找不到指定的数据。")
    return ResponseModel(code=200, data={"id": item_id}, msg="卡密删除成功")


"""
========================================
优惠券管理
========================================
"""


@app.get("/api/backend/coupon_read", tags=["TodoBackend"], dependencies=[Depends(DbUsers.current_superuser)])
async def coupon_read():
    """
    获取优惠券列表
    """
    return ResponseModel(code=200, data={"data": []}, msg="优惠券查询成功")


@app.post("/api/backend/coupon_create", tags=["TodoBackend"], dependencies=[Depends(DbUsers.current_superuser)])
async def coupon_create():
    """
    新增优惠券
    """
    return ResponseModel(code=200, data={}, msg="优惠券新增成功")


@app.patch("/api/backend/coupon_update", tags=["TodoBackend"], dependencies=[Depends(DbUsers.current_superuser)])
async def coupon_update():
    """
    修改优惠券
    """
    return ResponseModel(code=200, data={}, msg="优惠券修改成功")


@app.delete("/api/backend/coupon_delete", tags=["TodoBackend"], dependencies=[Depends(DbUsers.current_superuser)])
async def coupon_delete():
    """
    删除优惠券
    """
    return ResponseModel(code=200, data={}, msg="优惠券删除成功")


@app.patch("/api/backend/coupon_switch", tags=["TodoBackend"], dependencies=[Depends(DbUsers.current_superuser)])
async def coupon_switch():
    """
    开关优惠券
    """
    return ResponseModel(code=200, data={}, msg="优惠券开关成功")


"""
========================================
订单管理
========================================
"""


@app.get("/api/backend/order_read", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def order_read(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    获取订单列表
    """
    orders = db.read_datas(DbModels.Order, DbSchemas.OrderResponse, skip, limit)
    return ResponseModel(code=200, data=orders, msg="订单查询成功")


@app.post("/api/backend/order_search", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def order_search(cla: DbSchemas.OrderSearch, skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    搜索订单
    """
    filter_params = [or_(DbModels.Order.out_order_id.like(f"%{cla.out_order_id}%"),
                         DbModels.Order.contact.like(f"%{cla.contact}%"),
                         DbModels.Order.card.like(f"%{cla.card}%"))]
    orders = db.search_filter_page_turning(DbModels.Order, DbSchemas.OrderResponse, filter_params, skip, limit)
    return ResponseModel(code=200, data=orders, msg="订单查询成功")


@app.delete("/api/backend/order_delete", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def order_delete(cla: DbSchemas.OrderDelete):
    """
    删除订单
    """
    db.delete_data(DbModels.Order, cla.id)
    return ResponseModel(code=200, data={"id": cla.id}, msg="订单删除成功")


@app.delete("/api/backend/order_delete_all", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def order_delete_all():
    """
    删除订单
    """
    db.delete_batch_data(DbModels.Order, {"status": 0})
    return ResponseModel(code=200, data={}, msg="所有未完成订单删除成功")


"""
========================================
用户管理
========================================
"""


@app.get("/api/backend/user_read", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def user_read(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    获取用户列表
    """
    users = db.read_datas(DbModels.User, DbUsers.UserResponse, skip, limit)
    return ResponseModel(code=200, data=users, msg="用户查询成功")


@app.get("/api/backend/user_search/{userstr}", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def user_search(userstr: str, skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    搜索用户
    """
    filter_params = [or_(DbModels.User.email.like(f"%{userstr}%"))]
    users = db.search_filter_page_turning(DbModels.User, DbUsers.UserResponse, filter_params, skip, limit)
    return ResponseModel(code=200, data=users, msg="用户查询成功")


@app.patch("/api/backend/user_reset", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def user_reset(cla: DbUsers.UserID):
    """
    重置用户密码
    """
    return ResponseModel(code=200, data={"id": cla.id}, msg="用户密码重置成功(暂未实现)")


@app.delete("/api/backend/user_delete", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def user_delete(cla: DbUsers.UserID):
    """
    删除用户
    """
    db.delete_data(DbUsers.User, cla.id)
    return ResponseModel(code=200, data={"id": cla.id}, msg="用户删除成功")


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


@app.get("/api/backend/drawingbed_read", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def drawingbed_read(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
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
    res_data = {"records": data, "pager": {"page": skip, "pageSize": limit, "total": total_files}}
    return ResponseModel(code=200, data=res_data, msg="图像查询成功")


@app.get("/api/backend/drawingbed_show/{filename}", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def drawingbed_show(filename: str):
    file_location = Path(UPLOAD_DIR) / filename
    if file_location.exists():
        return responses.FileResponse(file_location)
    else:
        return ResponseModel(code=404, data={"file_location": file_location}, msg="找不到文件")


@app.post("/api/backend/drawingbed_create", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def drawingbed_create(file: UploadFile = File(...)):
    """
    新增图床
    """
    extension = file.filename.split(".")[-1]
    filename = generate_random_filename(extension)
    file_location = Path(UPLOAD_DIR) / filename
    with open(file_location, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return ResponseModel(code=200, data={"filename": filename, "file_location": file_location}, msg="图像上传成功")


@app.delete("/api/backend/drawingbed_delete/{filename}", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def drawingbed_delete(filename: str):
    """
    删除图床
    """
    file_location = Path(UPLOAD_DIR) / filename
    if file_location.exists():
        os.remove(file_location)
        return ResponseModel(code=200, data={"file_location": file_location}, msg="图像删除成功")
    else:
        return ResponseModel(code=404, data={"file_location": file_location}, msg="找不到文件")


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
    return ResponseModel(code=200, data={"data": []}, msg="佣金记录列表获取成功")


@app.get("/api/backend/invite_search", tags=["TodoBackend"])
async def search_invite():
    """
    搜索佣金记录
    """
    return ResponseModel(code=200, data={"data": []}, msg="搜索佣金记录")


@app.delete("/api/backend/invite_delete", tags=["TodoBackend"])
async def delete_invite():
    """
    删除佣金记录
    """
    return ResponseModel(code=200, data={"data": []}, msg="佣金记录删除成功")


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
    return ResponseModel(code=200, data={"data": []}, msg="主题设置获取成功")


class Theme(BaseModel):
    name: str
    description: Optional[str] = None


@app.patch("/api/backend/theme_update", tags=["TodoBackend"])
async def update_theme():
    """
    更新主题设置
    """
    return ResponseModel(code=200, data={"data": []}, msg="主题设置更新成功")


"""
========================================
支付接口设置
========================================
"""


@app.get("/api/backend/payment_read", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def payment_read(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    获取支付接口设置
    """
    temp_dic = {}
    payments = db.read_datas(DbModels.Payment, DbSchemas.PayResponse, skip, limit)
    temp_dic["pager"] = payments['pager']
    data = [payment.dict() for payment in payments['data']]
    res_data = {"records": data, "pager": temp_dic['pager']}
    return ResponseModel(code=200, data=res_data, msg="支付接口查询成功")


@app.patch("/api/backend/payment_update", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def payment_update(cla: DbSchemas.PayUpdate):
    """
    更新支付接口设置
    """
    cla.config = str(cla.config)
    data = dict(cla)
    record = db.update_data(DbModels.Payment, data)
    if record is None:
        return ResponseModel(code=500, data={}, msg="支付接口设置更新失败, 请检查修改的数据。")
    return ResponseModel(code=200, data=data, msg="支付接口设置更新成功")


@app.patch("/api/backend/payment_callback_update", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def payment_callback_update(callback: str):
    """
    更新支付接口设置
    """
    db.create_data(DbModels.Config(name="支付回调地址", info=callback, description="支付回调地址", isshow=True))
    return ResponseModel(code=200, data=callback, msg="支付回调地址保存成功")


"""
========================================
消息通知
========================================
"""


@app.get("/api/backend/message", tags=["TodoBackend"], dependencies=[Depends(DbUsers.current_superuser)])
async def get_message():
    """
    获取消息通知设置
    """
    return ResponseModel(code=200, data={"data": []}, msg="消息通知设置获取成功")


@app.post("/api/backend/send_email_test", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def send_email(addressee: str = 'admin@qq.com', subject: str = '测试邮件', content: str = '今日报告已生成，请查收。'):
    """
    测试SMTP
    """
    email_manager.send_email(addressee, subject, content)
    return ResponseModel(code=200, data={}, msg="测试邮件发送成功")


@app.patch("/api/backend/save_email_settings", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def save_email_settings(config: dict = {'sendname': 'no_replay', 'sendmail': 'demo@gmail.com',
                                              'smtp_address': 'smtp.163.com', 'smtp_port': '465',
                                              'smtp_pwd': 'ZZZZZZZ'}):
    """
    保存SMTP设置
    """
    try:
        dic = {"name": "邮箱通知", "config": str(config), "admin_account": "admin@qq.com"}
        db.update_data_name(DbModels.Notice, dic)
    except Exception:
        db.create_data(DbModels.Notice(name="邮箱通知", config=str(config), admin_account="admin@qq.com"))
    return ResponseModel(code=200, data=config, msg="SMTP设置保存成功")


@app.post("/api/backend/save_admin_setting", tags=["TodoBackend"])
async def save_admin_setting():
    """
    测试Admin消息
    """
    return ResponseModel(code=200, data={}, msg="Admin消息测试成功")


@app.patch("/api/backend/admin_message_test", tags=["TodoBackend"])
async def admin_message_test():
    """
    设置Admin消息
    """
    return ResponseModel(code=200, data={}, msg="Admin消息设置成功")


@app.patch("/api/backend/message_switch", tags=["TodoBackend"])
async def switch_message():
    """
    切换消息开关
    """
    return ResponseModel(code=200, data={}, msg="消息开关切换成功")


"""
========================================
综合设置
========================================
"""


@app.get("/api/backend/get_other_config", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def get_other_config():
    """
    获取综合设置
    """
    result = db.search_filter(DbModels.Config, DbSchemas.ConfigResponse, {})
    return ResponseModel(code=200, data=result, msg="综合设置查询成功")


@app.patch("/api/backend/home_notice", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def update_home_notice(home_notice: str):
    """
    更新店铺公告
    """
    dic = {"name": "home_notice", "info": home_notice, "description": "首页公告", "isshow": True}
    db.update_data_name(DbModels.Config, dic)
    return ResponseModel(code=200, data=dic, msg="首页公告更新成功")


@app.patch("/api/backend/icp", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def update_icp(icp: str):
    """
    更新底部备案
    """
    dic = {"name": "icp", "info": icp, "description": "底部备案", "isshow": True}
    db.update_data_name(DbModels.Config, dic)
    return ResponseModel(code=200, data=dic, msg="底部备案更新成功")


@app.patch("/api/backend/other_optional", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def update_other_optional(other_optional: dict = {"login_mode": 1, "tourist_orders": 1,
                                                        "front_desk_inventory_display": 1, "front_end_sales_display": 1,
                                                        "sales_statistics": 1}):
    """
    更新可选参数
    """
    dic = {"name": "other_optional", "info": str(other_optional), "description": "可选参数", "isshow": True}
    db.update_data_name(DbModels.Config, dic)
    return ResponseModel(code=200, data=dic, msg="可选参数更新成功")


@app.patch("/api/backend/admin_reset", tags=["TodoBackend"])
async def reset_admin_account():
    """
    管理员账密修改
    """
    return ResponseModel(code=200, data={"暂未实现": ""}, msg="管理员账密修改成功")


"""
========================================
返回商店主页
========================================
"""


@app.get("/api/backend/back_store", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def back_store():
    """
    返回商店主页
    """
    store_url = db.search_data(DbModels.Config, DbSchemas.ConfigResponseName, [DbModels.Config.name == 'store_url'])
    return ResponseModel(code=200, data=dict(store_url), msg="返回商店主页URL获取成功")


"""
========================================
退出登录
========================================
"""


@app.get("/api/backend/logout", tags=["backend"], dependencies=[Depends(DbUsers.current_superuser)])
async def logout(response: Response):
    """
    退出登录，清除COOKIE
    """
    response.delete_cookie(key="session")
    return ResponseModel(code=200, data={}, msg="退出登录成功")


"""
========================================
以下为前台页面
========================================
"""


@app.get("/api/frontend/homes", tags=["TodoFrontend"])
async def home(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10)):
    """
    获取首页商品信息
    """
    prodinfos = db.read_datas(DbModels.ProdInfo, DbSchemas.ProdInfoResponse, skip, limit)
    return ResponseModel(code=200, data=prodinfos, msg="获取首页商品信息成功")


@app.get("/api/frontend/user_invitation", tags=["TodoFrontend"])
async def user_invitation():
    """
    获取邀请好友信息接口
    """
    return ResponseModel(code=200, data={}, msg="邀请好友信息查询成功")


@app.get("/api/frontend/user_order", tags=["TodoFrontend"])
async def user_order(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10), user: DbUsers.User = Depends(DbUsers.current_active_user)):
    """
    获取个人中心信息接口 返回最近订单
    """
    orders = db.read_datas(DbModels.Order, DbSchemas.OrderResponse, skip, limit)
    return ResponseModel(code=200, data=orders, msg="用户订单信息查询成功")


@app.get("/api/frontend/user_payment_details", tags=["TodoFrontend"])
async def user_payment_details(skip: Optional[int] = Query(0), limit: Optional[int] = Query(10), user: DbUsers.User = Depends(DbUsers.current_active_user)):
    """
    获取订单中心信息接口
    """
    orders = db.read_datas(DbModels.Order, DbSchemas.OrderResponse, skip, limit)
    return ResponseModel(code=200, data=orders, msg="用户支付明细查询成功")


@app.get("/api/frontend/user_wallet", tags=["TodoFrontend"])
async def user_wallet(user: DbUsers.User = Depends(DbUsers.current_active_user)):
    """
    获取我的钱包信息接口
    """
    # Token 获取User email
    wallet_balance = db.search_data(DbUsers.User, DbUsers.UserMoney, [DbUsers.User.email == user.email])
    return ResponseModel(code=200, data=dict(wallet_balance), msg="我的钱包余额查询成功")


@app.get("/api/frontend/user_order_query", tags=["TodoFrontend"])
async def user_order_query(user: DbUsers.User = Depends(DbUsers.current_active_user)):
    """
    查询订单信息接口
    """
    return ResponseModel(code=200, data={}, msg="订单查询")


@app.get("/api/frontend/logout", tags=["TodoFrontend"], dependencies=[Depends(DbUsers.current_user)])
async def logout(response: Response):
    """
    用户退出登录接口，清除COOKIE
    """
    response.delete_cookie(key="session")
    return ResponseModel(code=200, data={}, msg="退出登录成功")


"""
返回给定身份验证后端的身份验证路由器。
：param backend:身份验证后端实例。
是否需要验证用户。默认为False。
"""
app.include_router(DbUsers.fastapi_users.get_auth_router(DbUsers.auth_backend),
                   prefix="/auth/jwt",
                   tags=["auth"])

"""
返回一个带有注册路由的路由器。
：param UserRead：公共用户的Pydantic架构。
：param UserCreate：用于创建用户的Pydantic架构。
"""
app.include_router(DbUsers.fastapi_users.get_register_router(DbUsers.UserRead, DbUsers.UserCreate),
                   prefix="/auth/jwt",
                   tags=["auth"],
                   )

"""
返回重置密码过程路由器。
"""
app.include_router(DbUsers.fastapi_users.get_reset_password_router(),
                   prefix="/auth/jwt",
                   tags=["auth"],
                   )

"""
返回一个带有电子邮件验证路由的路由器。
：param UserRead：公共用户的Pydantic架构。
"""
app.include_router(DbUsers.fastapi_users.get_verify_router(DbUsers.UserRead),
                   prefix="/auth/jwt",
                   tags=["auth"],
                   )

"""
返回一个带有路由的路由器来管理用户。
：param UserRead：公共用户的Pydantic架构。
：param UserUpdate：用于更新用户的Pydantic架构。
"""
app.include_router(DbUsers.fastapi_users.get_users_router(DbUsers.UserRead, DbUsers.UserUpdate),
                   prefix="/auth/jwt",
                   tags=["DbUsers"],
                   )


@app.get("/authenticated-route")
async def authenticated_route(user: DbUsers.User = Depends(DbUsers.current_active_user)):
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
