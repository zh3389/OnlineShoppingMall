from fastapi import Body
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
    name: str = Body(default="测试名称cag", description="【必填】分类的名称")
    sort: int = Body(default=0, description="【必填】分类排序的数值0～100")
    state: bool = Body(default=True, description="【必填】是否激活该类别，用于筛选该类别商品是否显示")


class ProdCagUpdate(ProdCagBase):
    id: int = Body(description="【必填】分类的唯一ID")
    name: Optional[str] = Body(default="测试名称cag", description="【可选】分类的名称")
    sort: Optional[int] = Body(default=0, description="【可选】分类排序的数值0～100")
    state: Optional[bool] = Body(default=True, description="【可选】是否激活该类别，用于筛选该类别商品是否显示")


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
    name: str = Body(default="测试添加名称info", description="【必填】产品的名称")
    prod_cag_name: Optional[str] = Body(description="【可选】产品的分类名称, 用于筛选商品是哪个类别的商品")
    prod_info: Optional[str] = Body(description="【可选】产品的描述信息")
    prod_img_url: Optional[str] = Body(description="【可选】""产品图片名称URL,上传图像后会返回名称")
    prod_discription: Optional[str] = Body(description="【可选】卡密使用教程")
    prod_price: float = Body(default=99.99, description="【必填】产品价格")
    prod_price_wholesale: Optional[str] = Body(description="【可选】产品批发价格显示str")
    prod_sales: Optional[int] = Body(description="【可选】产品销量")
    prod_tag: Optional[str] = Body(description="【可选】产品标签，例限时优惠")
    auto: bool = Body(default=False, description="【必填】是否自动发货")
    sort: Optional[int] = Body(description="【可选】产品排序优先级")
    state: bool = Body(default=False, description="【必填】是否展示该商品")


class ProdInfoUpdate(ProdInfoBase):
    id: int = Body(description="【必填】产品的唯一ID")
    name: Optional[str] = Body(description="【可选】产品的名称")
    prod_cag_name: Optional[str] = Body(description="【可选】产品的分类名称, 用于筛选商品是哪个类别的商品")
    prod_info: Optional[str] = Body(description="【可选】产品的描述信息")
    prod_img_url: Optional[str] = Body(description="【可选】""产品图片名称URL,上传图像后会返回名称")
    prod_discription: Optional[str] = Body(description="【可选】卡密使用教程")
    prod_price: Optional[float] = Body(description="【可选】产品价格")
    prod_price_wholesale: Optional[str] = Body(description="【可选】产品批发价格显示str")
    prod_sales: Optional[int] = Body(description="【可选】产品销量")
    prod_tag: Optional[str] = Body(description="【可选】产品标签，例限时优惠")
    auto: Optional[bool] = Body(description="【可选】是否自动发货")
    sort: Optional[int] = Body(description="【可选】产品排序优先级")
    state: Optional[bool] = Body(description="【可选】是否展示该商品")


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
    prod_name: str = Body(default="测试卡密名称", description="【必填】卡密名称")
    card: str = Body(default="测试卡密内容", description="【必填】卡密内容")
    reuse: Optional[bool] = Body(default=False, description="【必填】是否允许重复使用")


class CardUpdate(CardBase):
    id: int = Body(description="【必填】卡密ID")
    prod_name: Optional[str] = Body(description="【可选】卡密名称")
    card: Optional[str] = Body(description="【可选】卡密内容")
    reuse: Optional[bool] = Body(description="【可选】是否允许重复使用")


class CardResponse(CardUpdate):
    class Config:
        orm_mode = True
        from_attributes = True


class CardFilterDelete(CardBase):
    prod_name: Optional[str] = Body(description="【可选】商品名称")
    isused: Optional[bool] = Body(description="【可选】是否已使用")


"""
========================================
订单信息
========================================
"""


class OrderBase(BaseModel):
    pass


class OrderSearch(OrderBase):
    out_order_id: Optional[str] = Body(description="【可选】订单号")
    contact: Optional[str] = Body(description="【可选】用户联系方式")
    card: Optional[str] = Body(description="【可选】卡密内容")


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
    id: int = Body(description="【必填】订单ID")


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
    config: Optional[Dict] = Body(description="【可选】支付接口配置")
    isactive: Optional[bool] = Body(description="【可选】是否激活该支付方式")


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
