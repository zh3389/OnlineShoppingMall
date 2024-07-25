from datetime import datetime
import ast
from pydantic import BaseModel, Field
from typing import Optional, Dict


"""
========================================
Response 模板
========================================
"""


class ResponseModel(BaseModel):
    code: int
    data: Optional[Dict] = None
    msg: str


"""
========================================
产品分类 数据的验证和序列化
========================================
"""


class ProdCagBase(BaseModel):
    pass


class ProdCagCreate(ProdCagBase):
    name: str = "测试类别名称"
    sort: int = 50
    state: bool = True


class ProdCagUpdate(ProdCagBase):
    id: int
    name: Optional[str] = None
    sort: Optional[int] = None
    state: Optional[bool] = None


class ProdCagResponse(ProdCagBase):
    id: int
    name: str
    sort: int
    state: bool

    class Config:
        orm_mode = True
        from_attributes = True


"""
========================================
产品信息 数据的验证和序列化
========================================
"""


class ProdInfoBase(BaseModel):
    pass


class ProdInfoCreate(ProdInfoBase):
    name: str = "产品名称"
    prod_cag_name: str = "所属分类"
    prod_info: str = "商品描述"
    prod_img_url: str = "产品图片名称URL,上传图像后会返回名称"
    prod_discription: str = "卡密使用教程"
    prod_price: float = 9.99
    prod_price_wholesale: str = "产品批发价格显示str"
    prod_sales: int = 8
    prod_tag: str = "产品标签, 限时优惠"
    auto: bool = False
    sort: int = 50
    state: bool = False


class ProdInfoUpdate(ProdInfoBase):
    id: int
    name: Optional[str] = None
    prod_cag_name: Optional[str] = None
    prod_info: Optional[str] = None
    prod_img_url: Optional[str] = None
    prod_discription: Optional[str] = None
    prod_price: Optional[float] = None
    prod_price_wholesale: Optional[str] = None
    prod_sales: Optional[int] = None
    prod_tag: Optional[str] = None
    auto: Optional[bool] = None
    sort: Optional[int] = None
    state: Optional[bool] = None


class ProdInfoResponse(ProdInfoUpdate):

    class Config:
        orm_mode = True
        from_attributes = True


"""
========================================
卡密信息
========================================
"""


class CardBase(BaseModel):
    pass


class CardCreate(CardBase):
    prod_name: str = "商品名称"
    card: str = "卡密"
    reuse: Optional[bool] = False


class CardUpdate(CardBase):
    id: int
    prod_name: Optional[str] = None
    card: Optional[str] = None
    reuse: Optional[bool] = None


class CardResponse(CardUpdate):
    class Config:
        orm_mode = True
        from_attributes = True


class CardFilterDelete(CardBase):
    prod_name: Optional[str] = None
    isused: Optional[bool] = None


"""
========================================
订单信息
========================================
"""


class OrderBase(BaseModel):
    pass


class OrderSearch(OrderBase):
    out_order_id: Optional[str] = None
    contact: Optional[str] = None
    card: Optional[str] = None


class OrderResponse(OrderBase):
    id: int
    status: Optional[bool] = None
    out_order_id: Optional[str] = None  # 订单ID 必填
    name: Optional[str] = None  # 商品名 必填
    payment: Optional[str] = None  # 支付渠道 必填
    num: Optional[int] = None  # 数量 必填
    price: Optional[float] = None  # 价格 必填
    total_price: Optional[float] = None  # 总价 必填
    contact_txt: Optional[str] = None
    contact: Optional[str] = None
    card: Optional[str] = None
    updatetime: Optional[datetime] = None

    class Config:
        orm_mode = True
        from_attributes = True


class OrderDelete(OrderBase):
    id: int


"""
========================================
综合设置
========================================
"""


class ConfigBase(BaseModel):
    pass


class ConfigResponse(ConfigBase):
    id: int
    name: str
    info: str
    description: str
    isshow: bool

    class Config:
        orm_mode = True
        from_attributes = True


class ConfigResponseName(ConfigBase):
    info: str

    class Config:
        orm_mode = True
        from_attributes = True


"""
========================================
支付接口
========================================
"""


class PayBase(BaseModel):
    pass


class PyaId(PayBase):
    id: int


class PayUpdate(PyaId):
    config: Optional[Dict] = None
    isactive: Optional[bool] = None


class PayResponse(PyaId):
    name: str
    icon: str
    config: str
    info: str
    isactive: bool

    def dict(self, *args, **kwargs):
        data = super().dict(*args, **kwargs)
        try:
            data['config'] = ast.literal_eval(data['config'])
        except Exception:
            raise ValueError("config field must be a valid JSON string")
        return data

    class Config:
        orm_mode = True
        from_attributes = True


"""
========================================
系统通知
========================================
"""


class NoticeBase(BaseModel):
    pass


class NoticeResponse(NoticeBase):
    id: int
    name: str
    config: str
    admin_account: str
    admin_switch: bool
    user_switch: bool

    class Config:
        orm_mode = True
        from_attributes = True
