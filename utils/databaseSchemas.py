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
    data: dict
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


class ProdCagUpdate(ProdCagCreate):
    id: int = 1


class ProdCagResponse(ProdCagCreate):
    id: int = 1

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


class ProdInfoID(ProdInfoBase):
    id: int = 1


class ProdInfoCreate(ProdInfoBase):
    prod_cag_name: Optional[str] = Field(None, description="产品分类名称")
    prod_info: Optional[str] = Field(None, description="产品信息")
    prod_img_url: Optional[str] = Field(None, description="产品图片url")
    prod_discription: Optional[str] = Field(None, description="产品描述")
    prod_price_wholesale: Optional[str] = Field(None, description="产品批发价格")
    prod_sales: Optional[int] = Field(None, description="产品销量")
    prod_tag: Optional[str] = Field(None, description="产品标签")
    sort: Optional[int] = Field(None, description="排序")


class ProdInfoUpdate(ProdInfoCreate, ProdInfoID):
    name: Optional[str] = Field(None, description="产品名称")
    prod_price: Optional[float] = Field(None, description="产品价格")
    auto: Optional[bool] = Field(None, description="是否自动上架")
    state: Optional[bool] = Field(None, description="是否上架")


class ProdInfoResponse(ProdInfoCreate, ProdInfoID):
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


class CardID(CardBase):
    id: int


class CardCreate(CardBase):
    prod_name: str  # 必填
    card: str  # 必填
    reuse: Optional[bool] = False  # 默认False


class CardUpdate(CardID):
    prod_name: Optional[str] = None  # 必填
    card: Optional[str] = None  # 必填
    reuse: Optional[bool] = None  # 默认False


class CardResponse(CardID, CardCreate):
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
