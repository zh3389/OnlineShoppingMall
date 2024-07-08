from utils.databaseManager import ProdCag
from pydantic import BaseModel


"""产品分类 数据的验证和序列化"""


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


"""产品信息 数据的验证和序列化"""


class ProdInfoBase(BaseModel):
    name: str  # 必填
    prod_cag_name: str or None
    prod_info: str or None
    prod_img_url: str or None
    prod_discription: str or None
    prod_price: float  # 必填
    prod_price_wholesale: str or None
    prod_sales: int or None
    prod_tag: str or None
    auto: bool  # 必填
    sort: int or None
    state: bool  # 必填


class ProdInfoCreate(ProdInfoBase):
    pass


class ProdInfoResponse(ProdInfoBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


