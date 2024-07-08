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