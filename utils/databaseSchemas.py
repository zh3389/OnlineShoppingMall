from utils.databaseManager import ProdCag
from pydantic import BaseModel
from typing import Optional


"""
========================================
产品分类 数据的验证和序列化
========================================
"""


class ProdCagBase(BaseModel):
    name: str
    sort: int
    state: bool


class ProdCagCreate(ProdCagBase):
    pass


class ProdCagResponse(ProdCagBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


"""
========================================
产品信息 数据的验证和序列化
========================================
"""


class ProdInfoBase(BaseModel):
    name: str  # 必填
    prod_cag_name: Optional[str] = None
    prod_info: Optional[str] = None
    prod_img_url: Optional[str] = None
    prod_discription: Optional[str] = None
    prod_price: float  # 必填
    prod_price_wholesale: Optional[str] = None
    prod_sales: Optional[int] = None
    prod_tag: Optional[str] = None
    auto: bool  # 必填
    sort: Optional[int] = None
    state: bool  # 必填


class ProdInfoCreate(ProdInfoBase):
    pass


class ProdInfoResponse(ProdInfoBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


