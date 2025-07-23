from pydantic import BaseModel

class ItemCreate(BaseModel):
    item_name : str
    item_description: str
    item_price : float

    class Config:
        from_attributes = True


class ItemResponse(BaseModel):
    item_id: int
    item_name: str
    item_description: str
    item_price: float

    class Config:
        from_attributes = True
