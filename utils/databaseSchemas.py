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
    prod_cag_name: str | None
    prod_info: str | None
    prod_img_url: str | None
    prod_discription: str | None
    prod_price: float  # 必填
    prod_price_wholesale: str | None
    prod_sales: int | None
    prod_tag: str | None
    auto: bool  # 必填
    sort: int | None
    state: bool  # 必填


class ProdInfoCreate(ProdInfoBase):
    pass


class ProdInfoResponse(ProdInfoBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True


