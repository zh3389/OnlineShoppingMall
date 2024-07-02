import uvicorn
from typing import Optional, List
from pydantic import BaseModel
from fastapi import FastAPI, HTTPException, Request, Response, Depends, Form
from contextlib import asynccontextmanager
from utils.users import User, create_db_and_tables, UserCreate, UserRead, UserUpdate, auth_backend, current_active_user, fastapi_users
from fastapi.middleware.cors import CORSMiddleware
from utils.databaseDisplay import DisplayDataQuery, ProdCag

ddq = DisplayDataQuery('sqlite:///./utils/database.db')


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    一个上下文管理器，用于处理FastAPI应用程序的使用寿命。
    它创建了必要的数据库和表。
    参数：
        - app: FastAPI - 要使用的FastAPI实例。
    """
    # 如果您设置了像Alembic这样的迁移系统，则不需要
    await create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
# 配置 CORS
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:10000",
]

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
)


# 仪表盘
@app.get("/api/backend/dashboard", tags=["backend"])
async def get_dashboard():
    """
    获取仪表盘数据
    """
    result = ddq.query_dashboard_data()
    return result


# 分类管理
@app.get("/api/backend/classification", tags=["backend"])
async def get_classification():
    """
    获取分类列表
    """
    return {"message": "分类列表"}


class Classification(BaseModel):
    name: str
    description: Optional[str] = None


@app.post("/api/backend/class_add", tags=["backend"])
async def add_classification(classification: Classification):
    """
    新增分类
    """
    return {"message": "分类新增成功"}


@app.patch("/api/backend/class_update", tags=["backend"])
async def update_classification(classification: Classification):
    """
    修改分类
    """
    return {"message": "分类修改成功"}


@app.delete("/api/backend/class_delete", tags=["backend"])
async def delete_classification(class_id: int):
    """
    删除分类
    """
    return {"message": "分类删除成功"}


# 商品管理
@app.get("/api/backend/product", tags=["backend"])
async def get_products():
    """
    获取商品列表
    """
    return {"message": "商品列表"}


class Product(BaseModel):
    name: str
    price: float
    description: Optional[str] = None


@app.post("/api/backend/product_add", tags=["backend"])
async def add_product(product: Product):
    """
    新增商品
    """
    return {"message": "商品新增成功"}


@app.patch("/api/backend/product_update", tags=["backend"])
async def update_product(product: Product):
    """
    修改商品
    """
    return {"message": "商品修改成功"}


@app.delete("/api/backend/product_delete", tags=["backend"])
async def delete_product(product_id: int):
    """
    删除商品
    """
    return {"message": "商品删除成功"}


# 卡密管理
@app.get("/api/backend/cami", tags=["backend"])
async def get_cami():
    """
    获取卡密列表
    """
    return {"message": "卡密列表"}


class Cami(BaseModel):
    code: str
    description: Optional[str] = None


@app.post("/api/backend/cami_add", tags=["backend"])
async def add_cami(cami: Cami):
    """
    新增卡密
    """
    return {"message": "卡密新增成功"}


@app.patch("/api/backend/cami_update", tags=["backend"])
async def update_cami(cami: Cami):
    """
    修改卡密
    """
    return {"message": "卡密修改成功"}


@app.delete("/api/backend/cami_delete", tags=["backend"])
async def delete_cami(cami_id: int):
    """
    删除卡密
    """
    return {"message": "卡密删除成功"}


# 优惠券管理
@app.get("/api/backend/coupon", tags=["backend"])
async def get_coupons():
    """
    获取优惠券列表
    """
    return {"message": "优惠券列表"}


class Coupon(BaseModel):
    code: str
    discount: float
    description: Optional[str] = None


@app.post("/api/backend/coupon_add", tags=["backend"])
async def add_coupon(coupon: Coupon):
    """
    新增优惠券
    """
    return {"message": "优惠券新增成功"}


@app.patch("/api/backend/coupon_update", tags=["backend"])
async def update_coupon(coupon: Coupon):
    """
    修改优惠券
    """
    return {"message": "优惠券修改成功"}


@app.delete("/api/backend/coupon_delete", tags=["backend"])
async def delete_coupon(coupon_id: int):
    """
    删除优惠券
    """
    return {"message": "优惠券删除成功"}


# 订单管理
@app.get("/api/backend/order", tags=["backend"])
async def get_orders():
    """
    获取订单列表
    """
    return {"message": "订单列表"}


@app.get("/api/backend/order_search", tags=["backend"])
async def search_orders(keyword: str):
    """
    搜索订单
    """
    return {"message": "搜索订单"}


@app.delete("/api/backend/order_delete", tags=["backend"])
async def delete_order(order_id: int):
    """
    删除订单
    """
    return {"message": "订单删除成功"}


# 用户管理
@app.get("/api/backend/user", tags=["backend"])
async def get_users():
    """
    获取用户列表
    """
    return {"message": "用户列表"}


@app.get("/api/backend/user_search", tags=["backend"])
async def search_users(keyword: str):
    """
    搜索用户
    """
    return {"message": "搜索用户"}


@app.patch("/api/backend/user_reset", tags=["backend"])
async def reset_user_password(user_id: int):
    """
    重置用户密码
    """
    return {"message": "用户密码重置成功"}


@app.delete("/api/backend/user_delete", tags=["backend"])
async def delete_user(user_id: int):
    """
    删除用户
    """
    return {"message": "用户删除成功"}


# 图床管理
@app.get("/api/backend/drawingbed", tags=["backend"])
async def get_drawingbed():
    """
    获取图床列表
    """
    return {"message": "图床列表"}


class Drawingbed(BaseModel):
    url: str
    description: Optional[str] = None


@app.post("/api/backend/drawingbed_add", tags=["backend"])
async def add_drawingbed(drawingbed: Drawingbed):
    """
    新增图床
    """
    return {"message": "图床新增成功"}


@app.delete("/api/backend/drawingbed_delete", tags=["backend"])
async def delete_drawingbed(drawingbed_id: int):
    """
    删除图床
    """
    return {"message": "图床删除成功"}


# 佣金记录
@app.get("/api/backend/invite", tags=["backend"])
async def get_invite():
    """
    获取佣金记录列表
    """
    return {"message": "佣金记录列表"}


@app.get("/api/backend/invite_search", tags=["backend"])
async def search_invite(keyword: str):
    """
    搜索佣金记录
    """
    return {"message": "搜索佣金记录"}


@app.delete("/api/backend/invite_delete", tags=["backend"])
async def delete_invite(invite_id: int):
    """
    删除佣金记录
    """
    return {"message": "佣金记录删除成功"}


# 主题设置
@app.get("/api/backend/theme", tags=["backend"])
async def get_theme():
    """
    获取主题设置
    """
    return {"message": "主题设置"}


class Theme(BaseModel):
    name: str
    description: Optional[str] = None


@app.patch("/api/backend/theme_update", tags=["backend"])
async def update_theme(theme: Theme):
    """
    更新主题设置
    """
    return {"message": "主题设置更新成功"}


# 支付接口
@app.get("/api/backend/payment", tags=["backend"])
async def get_payment():
    """
    获取支付接口设置
    """
    return {"message": "支付接口设置"}


@app.patch("/api/backend/payment_update", tags=["backend"])
async def update_payment(payment: dict):
    """
    更新支付接口设置
    """
    return {"message": "支付接口设置更新成功"}


# 消息通知
@app.get("/api/backend/message", tags=["backend"])
async def get_message():
    """
    获取消息通知设置
    """
    return {"message": "消息通知设置"}


@app.post("/api/backend/message_smtp_test", tags=["backend"])
async def send_smtp():
    """
    测试SMTP
    """
    return {"message": "SMTP测试成功"}


@app.patch("/api/backend/message_smtp_save", tags=["backend"])
async def save_smtp_settings(settings: dict):
    """
    保存SMTP设置
    """
    return {"message": "SMTP设置保存成功"}


@app.post("/api/backend/message_admin_test", tags=["backend"])
async def send_admin_message():
    """
    测试Admin消息
    """
    return {"message": "Admin消息测试成功"}


@app.patch("/api/backend/message_admin_set", tags=["backend"])
async def set_admin_message(settings: dict):
    """
    设置Admin消息
    """
    return {"message": "Admin消息设置成功"}


@app.patch("/api/backend/message_switch", tags=["backend"])
async def switch_message(status: bool):
    """
    切换消息开关
    """
    return {"message": "消息开关切换成功"}


# 综合设置
@app.get("/api/backend/other", tags=["backend"])
async def get_other():
    """
    获取综合设置
    """
    return {"message": "综合设置"}


@app.patch("/api/backend/shop_notice", tags=["backend"])
async def update_shop_notice(notice: str):
    """
    更新店铺公告
    """
    return {"message": "店铺公告更新成功"}


@app.patch("/api/backend/icp", tags=["backend"])
async def update_icp(icp_info: str):
    """
    更新底部备案
    """
    return {"message": "底部备案更新成功"}


@app.patch("/api/backend/other_optional", tags=["backend"])
async def update_other_optional(options: dict):
    """
    更新可选参数
    """
    return {"message": "可选参数更新成功"}


@app.patch("/api/backend/admin_reset", tags=["backend"])
async def reset_admin_account(admin_info: dict):
    """
    管理员账密修改
    """
    return {"message": "管理员账密修改成功"}


# 返回商店主页
@app.get("/api/backend/home", tags=["backend"])
async def return_home():
    """
    返回商店主页
    """
    return {"message": "返回商店主页"}


# 退出登录
@app.get("/api/backend/logout", tags=["backend"])
async def logout():
    """
    退出登录，清除COOKIE
    """
    return {"message": "退出登录成功"}


# 模拟数据库
users_db = {}
orders_db = {}


# 请求数据模型
class UserRegisterModel(BaseModel):
    username: str
    password: str
    email: str


class UserLoginModel(BaseModel):
    username: str
    password: str


class UserForgetPasswordModel(BaseModel):
    email: str


class UserResetPasswordModel(BaseModel):
    username: str
    new_password: str


# 首页
@app.get("/api/frontend/home", tags=["frontend"])
async def get_home():
    """
    获取首页数据
    """
    return {"message": "欢迎来到首页"}


# 用户注册
@app.post("/api/frontend/user_register", tags=["frontend"])
async def user_register(user: UserRegisterModel):
    """
    用户注册接口
    """
    if user.username in users_db:
        raise HTTPException(status_code=400, detail="用户名已存在")
    users_db[user.username] = {"password": user.password, "email": user.email}
    return {"message": "注册成功"}


# 用户登录
@app.post("/api/frontend/user_login", tags=["frontend"])
async def user_login(user: UserLoginModel):
    """
    用户登录接口
    """
    if user.username not in users_db or users_db[user.username]["password"] != user.password:
        raise HTTPException(status_code=400, detail="用户名或密码错误")
    return {"message": "登录成功"}


# 忘记密码
@app.post("/api/frontend/user_forgetpassword", tags=["frontend"])
async def user_forget_password(user: UserForgetPasswordModel):
    """
    用户忘记密码接口
    """
    for username, info in users_db.items():
        if info["email"] == user.email:
            return {"message": "重置密码邮件已发送"}
    raise HTTPException(status_code=404, detail="邮箱未注册")


# 邀请好友
@app.get("/api/frontend/user_invitation", tags=["frontend"])
async def user_invitation():
    """
    获取邀请好友信息接口
    """
    return {"message": "邀请好友"}


# 个人中心
@app.get("/api/frontend/user_center", tags=["frontend"])
async def user_center():
    """
    获取个人中心信息接口
    """
    return {"message": "个人中心"}


# 我的钱包
@app.get("/api/frontend/user_wallet", tags=["frontend"])
async def user_wallet():
    """
    获取我的钱包信息接口
    """
    return {"message": "我的钱包"}


# 重置密码
@app.patch("/api/frontend/user_reset", tags=["frontend"])
async def user_reset_password(user: UserResetPasswordModel):
    """
    用户重置密码接口
    """
    if user.username not in users_db:
        raise HTTPException(status_code=404, detail="用户未注册")
    users_db[user.username]["password"] = user.new_password
    return {"message": "密码重置成功"}


# 订单中心
@app.get("/api/frontend/user_order", tags=["frontend"])
async def user_order():
    """
    获取订单中心信息接口
    """
    return {"message": "订单中心"}


# 订单查询
@app.get("/api/frontend/user_order_query", tags=["frontend"])
async def user_order_query(order_id: Optional[int] = None):
    """
    查询订单信息接口
    """
    if order_id is not None and order_id in orders_db:
        return orders_db[order_id]
    return {"message": "订单查询"}


# 退出登录
@app.get("/api/frontend/logout", tags=["frontend"])
async def logout(response: Response):
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
